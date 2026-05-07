#!/usr/bin/env bash
# swarm-init.sh — одноразовая инициализация Docker Swarm на VPS
# ref: spec.md → Docker Swarm, Traefik v3, mydomain.ru
#
# Запуск: ssh root@<VPS_IP> 'bash -s' < scripts/swarm-init.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

VPS_IP="${1:?Usage: swarm-init.sh <VPS_PUBLIC_IP>}"
STACK_DIR="/opt/myapp"

echo "==> [1/7] Initializing Docker Swarm (single-node MVP)"
docker swarm init --advertise-addr "$VPS_IP" 2>/dev/null || echo "Swarm already initialized"

# Node label для будущей multi-node миграции (статeful сервисы)
MANAGER_ID=$(docker node ls --filter role=manager --format "{{.ID}}" | head -1)
docker node update --label-add role=db     "$MANAGER_ID"
docker node update --label-add role=broker "$MANAGER_ID"
echo "    Node $MANAGER_ID labeled: role=db, role=broker"

echo "==> [2/7] Creating stack directory"
mkdir -p "$STACK_DIR"/{traefik,rabbitmq,monitoring/grafana/provisioning,certs}

echo "==> [3/7] Creating Docker secrets"
echo "    IMPORTANT: Enter values when prompted, or press Ctrl+C and set manually."
echo ""

_create_secret() {
  local name="$1"
  local prompt="$2"
  if docker secret inspect "$name" &>/dev/null; then
    echo "    Secret '$name' already exists — skipping"
    return
  fi
  printf "    %s: " "$prompt"
  read -rs value
  echo
  printf '%s' "$value" | docker secret create "$name" -
  echo "    ✓ Secret '$name' created"
}

_create_secret postgres_password  "PostgreSQL password"
_create_secret rabbitmq_password  "RabbitMQ password"
_create_secret mailgun_api_key    "Mailgun API key"
_create_secret s3_access_key      "Yandex Cloud S3 Access Key ID"
_create_secret s3_secret_key      "Yandex Cloud S3 Secret Access Key"
_create_secret jwt_secret         "JWT secret (or press Enter to auto-generate)"

# Auto-generate JWT secret if empty
if ! docker secret inspect jwt_secret &>/dev/null; then
  openssl rand -hex 64 | docker secret create jwt_secret -
  echo "    ✓ jwt_secret auto-generated"
fi

echo "    Traefik basic-auth (htpasswd format):"
printf "    Admin username [admin]: "
read -r htuser
htuser="${htuser:-admin}"
printf "    Admin password: "
read -rs htpass
echo
printf '%s' "$(htpasswd -nbB "$htuser" "$htpass")" | docker secret create traefik_users -
echo "    ✓ traefik_users secret created"

echo "==> [4/7] Setting up acme.json for Let's Encrypt"
touch "$STACK_DIR/traefik/acme.json"
chmod 600 "$STACK_DIR/traefik/acme.json"

echo "==> [5/7] Copying config files (run from project root on local machine)"
echo "    scp -r traefik/ rabbitmq/ monitoring/ docker-stack.yml root@$VPS_IP:$STACK_DIR/"
echo "    (skipping — run this locally)"

echo "==> [6/7] Creating overlay networks"
docker network create --driver overlay --attachable myapp_frontend 2>/dev/null || true
docker network create --driver overlay --attachable myapp_backend  2>/dev/null || true
docker network create --driver overlay myapp_database              2>/dev/null || true
docker network create --driver overlay myapp_monitoring            2>/dev/null || true

echo "==> [7/7] UFW firewall rules"
if command -v ufw &>/dev/null; then
  ufw allow 22/tcp    # SSH
  ufw allow 80/tcp    # HTTP → HTTPS redirect
  ufw allow 443/tcp   # HTTPS + WSS
  ufw allow 2377/tcp  # Swarm manager (for future multi-node)
  ufw allow 7946/tcp  # Swarm node communication
  ufw allow 7946/udp
  ufw allow 4789/udp  # Swarm overlay network
  # IMPORTANT: 5432 (postgres), 5672 (rabbitmq), 15672 (rabbitmq-mgmt)
  # must NOT be open to public — they're on overlay network only
  ufw --force enable
  echo "    UFW rules applied"
fi

echo ""
echo "✅ Swarm initialized. Next step:"
echo "   Push code → GitHub Actions → auto-deploys to this VPS"
echo ""
echo "   Manual deploy (first time):"
echo "   IMAGE_TAG=latest GITHUB_REPO=org/repo \\"
echo "   docker stack deploy --with-registry-auth -c $STACK_DIR/docker-stack.yml myapp"
