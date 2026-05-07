# ─────────────────────────────────────────────────────────────────────────────
# Makefile — команды для локальной разработки
# Требования: docker, docker compose v2, pnpm, uv
# ─────────────────────────────────────────────────────────────────────────────

COMPOSE      := docker compose -f docker-compose.dev.yml --env-file .env.dev
BACKEND_DIR  := apps/backend
FRONTEND_DIR := apps/frontend

.PHONY: help dev-up dev-down dev-reset dev-logs dev-ps \
        db-migrate db-rollback db-shell \
        worker-emails worker-reports worker-files \
        api lint test

# ─── Help ────────────────────────────────────────────────────────────────────
help: ## Показать список команд
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
	  awk 'BEGIN{FS=":.*##"} {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  Dev URLs (после make dev-up):"
	@echo "    PostgreSQL   localhost:5432  (myapp / devpassword)"
	@echo "    RabbitMQ     localhost:5672  UI: http://localhost:15672"
	@echo "    MinIO S3     localhost:9000  Console: http://localhost:9001"
	@echo "    Mailpit      localhost:1025  UI: http://localhost:8025"

# ─── Инфраструктура ──────────────────────────────────────────────────────────
dev-up: ## Запустить инфраструктурные сервисы (postgres, rabbitmq, minio, mailpit)
	$(COMPOSE) up -d --remove-orphans
	@echo ""
	@echo "\033[32m✓ Инфраструктура запущена\033[0m"
	@echo "  RabbitMQ UI: http://localhost:15672  (myapp/devpassword)"
	@echo "  MinIO:       http://localhost:9001   (minioadmin/minioadmin)"
	@echo "  Mailpit:     http://localhost:8025"
	@echo ""
	@echo "Следующий шаг: make db-migrate && make api"

dev-down: ## Остановить сервисы (данные сохраняются)
	$(COMPOSE) down

dev-reset: ## Остановить сервисы и удалить все данные (volumes) — необратимо!
	$(COMPOSE) down -v
	$(COMPOSE) up -d --remove-orphans

dev-logs: ## Логи всех сервисов (follow)
	$(COMPOSE) logs -f

dev-logs-%: ## Логи конкретного сервиса: make dev-logs-postgres
	$(COMPOSE) logs -f $*

dev-ps: ## Статус сервисов
	$(COMPOSE) ps

# ─── База данных ─────────────────────────────────────────────────────────────
db-migrate: ## Применить все Alembic-миграции
	cd $(BACKEND_DIR) && uv run alembic upgrade head

db-rollback: ## Откатить последнюю миграцию
	cd $(BACKEND_DIR) && uv run alembic downgrade -1

db-makemigration: ## Сгенерировать миграцию: make db-makemigration m="add_users_table"
	cd $(BACKEND_DIR) && uv run alembic revision --autogenerate -m "$(m)"

db-shell: ## Открыть psql
	$(COMPOSE) exec postgres psql -U myapp -d myapp_dev

db-history: ## История миграций
	cd $(BACKEND_DIR) && uv run alembic history --verbose

# ─── S3 (MinIO) ──────────────────────────────────────────────────────────────
minio-init: ## Создать бакет myapp-dev (если minio-init контейнер не отработал)
	docker run --rm --network host \
	  minio/mc:latest \
	  /bin/sh -c " \
	    mc alias set local http://localhost:9000 minioadmin minioadmin && \
	    mc mb --ignore-existing local/myapp-dev && \
	    echo 'Done.' \
	  "

minio-lifecycle: ## Применить lifecycle policies (удаление tmp/24ч, архив reports/90д)
	cd $(BACKEND_DIR) && uv run python -c \
	  "import asyncio; from app.core.storage import set_lifecycle_policy; asyncio.run(set_lifecycle_policy())"

# ─── FastAPI ─────────────────────────────────────────────────────────────────
api: ## Запустить FastAPI dev-сервер (hot-reload)
	cd $(BACKEND_DIR) && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ─── Celery Workers ──────────────────────────────────────────────────────────
# ref: spec.md → emails (high-priority), reports (default), files (low-priority)
worker-emails: ## Celery worker для очереди emails
	cd $(BACKEND_DIR) && uv run celery -A app.celery_app worker \
	  -Q emails -c 2 --loglevel=debug -n emails@%h

worker-reports: ## Celery worker для очереди reports
	cd $(BACKEND_DIR) && uv run celery -A app.celery_app worker \
	  -Q reports -c 1 --loglevel=debug -n reports@%h

worker-files: ## Celery worker для очереди files
	cd $(BACKEND_DIR) && uv run celery -A app.celery_app worker \
	  -Q files -c 1 --loglevel=debug -n files@%h

worker-all: ## Celery worker для всех очередей (удобно для dev)
	cd $(BACKEND_DIR) && uv run celery -A app.celery_app worker \
	  -Q emails,reports,files,celery -c 4 --loglevel=debug

worker-monitor: ## Celery Flower — мониторинг задач в браузере (http://localhost:5555)
	cd $(BACKEND_DIR) && uv run celery -A app.celery_app flower --port=5555

# ─── Frontend ────────────────────────────────────────────────────────────────
dev: ## Запустить Nuxt dev-сервер
	cd $(FRONTEND_DIR) && pnpm dev

build-front: ## Собрать Nuxt для production
	cd $(FRONTEND_DIR) && pnpm build

# ─── Линтинг и тесты ─────────────────────────────────────────────────────────
lint: ## Запустить все линтеры (Biome + Ruff)
	cd $(FRONTEND_DIR) && pnpm biome check .
	cd $(BACKEND_DIR) && uv run ruff check . && uv run ruff format --check .

lint-fix: ## Автоисправление (Biome + Ruff)
	cd $(FRONTEND_DIR) && pnpm biome check --write .
	cd $(BACKEND_DIR) && uv run ruff check --fix . && uv run ruff format .

test: ## Vitest + Pytest
	cd $(FRONTEND_DIR) && pnpm vitest run
	cd $(BACKEND_DIR) && uv run pytest tests/ -v

test-watch: ## Vitest в watch-режиме
	cd $(FRONTEND_DIR) && pnpm vitest

# ─── Инсталляция зависимостей ────────────────────────────────────────────────
install: ## Установить JS-зависимости (pnpm)
	pnpm install

install-py: ## Установить Python-зависимости (uv sync) — запускать после создания apps/backend
	cd $(BACKEND_DIR) && uv sync --all-packages

# ─── Быстрый старт ───────────────────────────────────────────────────────────
bootstrap: dev-up install ## Первый запуск: dev-up + pnpm install; затем make install-py && make db-migrate
	@echo ""
	@echo "\033[32m✓ Готово к разработке!\033[0m"
	@echo "  make api          — запустить FastAPI"
	@echo "  make worker-all   — запустить Celery workers"
	@echo "  make dev          — запустить Nuxt"
