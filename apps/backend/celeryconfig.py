"""
Celery configuration — production settings.
ref: spec.md → Task Queue & Messaging (Production Config)

Secrets are read from Docker secrets files at /run/secrets/.
Falls back to env vars for local dev (CELERY_TASK_ALWAYS_EAGER=true).
"""

from __future__ import annotations

import os
from pathlib import Path

from kombu import Exchange, Queue


def _read_secret(name: str, env_fallback: str = "") -> str:
    path = Path(f"/run/secrets/{name}")
    if path.exists():
        return path.read_text().strip()
    return os.getenv(env_fallback, "")


# ─── Broker & Result Backend ────────────────────────────────────────────────────
# ref: spec.md → RabbitMQ as Celery Message Broker
_rmq_user = os.getenv("RABBITMQ_USER", "guest")
_rmq_pass = _read_secret("rabbitmq_password", "RABBITMQ_PASSWORD")
_rmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

broker_url = f"amqp://{_rmq_user}:{_rmq_pass}@{_rmq_host}:5672//"

# ref: spec.md → rpc:// Result Backend with result_expires=3600
result_backend = "rpc://"
result_expires = 3600
result_persistent = True  # survive broker restart

# ─── Serialization ──────────────────────────────────────────────────────────────
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

# ─── Worker Settings ────────────────────────────────────────────────────────────
# ref: spec.md → worker_prefetch_multiplier=4, worker_max_tasks_per_child=1000
worker_prefetch_multiplier = 4
worker_max_tasks_per_child = 1000
worker_disable_rate_limits = False

# ─── Exchanges ──────────────────────────────────────────────────────────────────
_emails_exchange = Exchange("emails", type="direct", durable=True)
_reports_exchange = Exchange("reports", type="direct", durable=True)
_files_exchange = Exchange("files", type="direct", durable=True)
_celery_exchange = Exchange("celery", type="direct", durable=True)

# ref: spec.md → Dead-Letter Exchange for failed tasks
_dlx_exchange = Exchange("dead_letters", type="direct", durable=True)

# ─── Queues ──────────────────────────────────────────────────────────────────────
# ref: spec.md → MVP Task Routing with DLX
task_queues = (
    # ref: spec.md → emails: High-priority queue, Mailgun HTTP API, rate-limit 10/s
    Queue(
        "emails",
        exchange=_emails_exchange,
        routing_key="emails",
        queue_arguments={
            "x-dead-letter-exchange": "dead_letters",
            "x-dead-letter-routing-key": "emails.dlx",
            "x-max-priority": 10,
            "x-message-ttl": 300_000,  # 5 min — email tasks should not queue long
            "x-queue-type": "classic",
        },
    ),
    # ref: spec.md → reports: Default queue, task_time_limit=300, WS progress broadcast
    Queue(
        "reports",
        exchange=_reports_exchange,
        routing_key="reports",
        queue_arguments={
            "x-dead-letter-exchange": "dead_letters",
            "x-dead-letter-routing-key": "reports.dlx",
            "x-message-ttl": 600_000,  # 10 min
            "x-queue-type": "classic",
        },
    ),
    # ref: spec.md → files: Low-priority queue, chunked processing, auto-cleanup
    Queue(
        "files",
        exchange=_files_exchange,
        routing_key="files",
        queue_arguments={
            "x-dead-letter-exchange": "dead_letters",
            "x-dead-letter-routing-key": "files.dlx",
            "x-message-ttl": 86_400_000,  # 24h — large file processing can queue
            "x-max-priority": 1,
            "x-queue-type": "classic",
        },
    ),
    # Default Celery queue
    Queue(
        "celery",
        exchange=_celery_exchange,
        routing_key="celery",
        queue_arguments={
            "x-dead-letter-exchange": "dead_letters",
            "x-dead-letter-routing-key": "celery.dlx",
        },
    ),
    # DLX capture queues — monitored by Prometheus celery-exporter + Grafana alerts
    Queue("emails.dlx", exchange=_dlx_exchange, routing_key="emails.dlx"),
    Queue("reports.dlx", exchange=_dlx_exchange, routing_key="reports.dlx"),
    Queue("files.dlx", exchange=_dlx_exchange, routing_key="files.dlx"),
    Queue("celery.dlx", exchange=_dlx_exchange, routing_key="celery.dlx"),
)

task_default_queue = "celery"
task_default_exchange = "celery"
task_default_routing_key = "celery"

# ─── Task Routing ────────────────────────────────────────────────────────────────
# ref: spec.md → MVP Task Routing (emails, reports, files)
task_routes = {
    "app.tasks.email.*": {"queue": "emails", "routing_key": "emails"},
    "app.tasks.report.*": {"queue": "reports", "routing_key": "reports"},
    "app.tasks.file.*": {"queue": "files", "routing_key": "files"},
}

# ─── Task Annotations (per-task defaults) ───────────────────────────────────────
task_annotations = {
    # ref: spec.md → emails: rate-limit 10/s, retry on 5xx, DLX on hard-bounce
    "app.tasks.email.*": {
        "rate_limit": "10/s",
        "max_retries": 3,
        "default_retry_delay": 60,
        "autoretry_for": (Exception,),
        "retry_backoff": True,
        "retry_backoff_max": 300,
        "retry_jitter": True,
        "acks_late": True,
        "reject_on_worker_lost": True,
    },
    # ref: spec.md → reports: task_time_limit=300, WS progress broadcast
    "app.tasks.report.*": {
        "time_limit": 300,
        "soft_time_limit": 270,
        "acks_late": True,
        "reject_on_worker_lost": True,
        "track_started": True,
    },
    # ref: spec.md → files: chunked processing, auto-cleanup on completion/failure
    "app.tasks.file.*": {
        "rate_limit": "5/s",
        "max_retries": 3,
        "default_retry_delay": 30,
        "acks_late": True,
        "reject_on_worker_lost": True,
    },
}

# ─── Observability ───────────────────────────────────────────────────────────────
task_track_started = True
task_send_sent_event = True
worker_send_task_events = True

# ─── Reliability ─────────────────────────────────────────────────────────────────
# ref: spec.md → At-Least-Once Delivery + Idempotent Task Design
task_acks_late = True
task_reject_on_worker_lost = True
broker_connection_retry_on_startup = True
broker_connection_max_retries = 10
broker_heartbeat = 60
broker_pool_limit = 10

# ─── Local dev override ──────────────────────────────────────────────────────────
if os.getenv("CELERY_TASK_ALWAYS_EAGER") == "true":
    task_always_eager = True
    task_eager_propagates = True
