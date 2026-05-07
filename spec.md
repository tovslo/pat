# Technical Specification: Self-Hosted Web Application Monorepo (Production-Ready)

## 📦 Frontend Core

**Nuxt 3 + Vue 3 + TypeScript**
- **Назначение:** SSR/SSG фреймворк с реактивным компонентным движком и строгой типизацией.
- **Обоснование:** Nuxt предоставляет роутинг «из коробки», встроенную оптимизацию производительности и глубокую интеграцию с экосистемой Vue 3. TypeScript гарантирует безопасность типов на этапе компиляции.
- **Архитектурные паттерны:** File-based routing, Composition API, Feature-Sliced Design (FSD), Server/Client boundary separation.

**Tailwind CSS + @nuxt/ui + Lucide Icons**
- **Назначение:** Utility-first стилизация, готовый UI-кит, векторные иконки.
- **Обоснование:** Tailwind минимизирует размер CSS-файлов и ускоряет верстку. `@nuxt/ui` обеспечивает нативную интеграцию с Nuxt 3. Lucide легковесен, модулен и легко кастомизируется.
- **Архитектурные паттерны:** Design Tokens, Atomic CSS, Component Composition over inheritance.

**@vueuse/core**
- **Назначение:** Набор утилитарных композиций для работы с DOM, состоянием браузера и реактивностью.
- **Обоснование:** Экономит время на реализации базовых хуков (resize, debounce, local storage, dark mode, WebSockets, S3 presigned uploads).
- **Архитектурные паттерны:** Pure Composables, Side-effect isolation, Reactive primitives encapsulation.

**pnpm + Turborepo**
- **Назначение:** Менеджер пакетов и система оркестрации задач монорепозитория.
- **Обоснование:** `pnpm` экономит дисковое пространство и ускоряет установку через жесткие ссылки. `Turborepo` кэширует задачи и параллелит сборки, значительно сокращая время CI/CD.
- **Архитектурные паттерны:** Workspace Isolation, Remote Caching, Task Pipeline Dependency Graph, Monorepo Boundary Enforcement.

---

## 🗃️ State & Validation

**Pinia**
- **Назначение:** Управление состоянием приложения.
- **Обоснование:** Официальный state manager для Vue 3, легковесный, поддерживает SSR и отлично интегрируется с DevTools.
- **Архитектурные паттерны:** Domain-scoped stores, Composition API setup syntax, State Normalization, Unidirectional Data Flow.

**Zod + vee-validate + openapi-fetch + openapi-typescript**
- **Назначение:** Валидация данных, управление формами, типизированные HTTP-клиенты.
- **Обоснование:** Zod обеспечивает runtime-валидацию. `openapi-typescript` генерирует типы из схемы, `openapi-fetch` создает type-safe клиент. `vee-validate` связывает валидацию с UI-формами.
- **Архитектурные паттерны:** Single Source of Truth (OpenAPI → TS Types → Zod Schemas), Form-State Binding, Contract-First API, Runtime Type Guards.

**@nuxt/auth-utils**
- **Назначение:** Аутентификация и управление сессиями.
- **Обоснование:** Нативная поддержка OAuth2, JWT, email/password и бесшовная интеграция с Nuxt Server API.
- **Архитектурные паттерны:** Session Management via HTTP-only cookies (Secure, SameSite=Lax/Strict, Domain=`mydomain.ru`), RBAC, Token Rotation & Refresh Flow.

---

## 📡 Real-time Communication (WebSockets)

**FastAPI WebSockets + Nuxt WS Client**
- **Назначение:** Двусторонний канал для push-уведомлений о статусе фоновых задач в реальном времени.
- **Обоснование:** Нативная поддержка в FastAPI/Starlette и легкая интеграция в Nuxt через `@vueuse/core/useWebSocket`. Минимизирует polling-трафик и улучшает UX.
- **Архитектурные паттерны:** Connection Manager with Auth Handshake, Heartbeat/Ping-Pong (Keep-alive), Graceful Reconnection with Exponential Backoff, Fallback to HTTP Polling on WS failure.

---

## 🧪 Testing & Linting

**Vitest + Playwright**
- **Назначение:** Unit/Component тестирование и E2E тестирование.
- **Обоснование:** Vitest нативен для Vite/Nuxt и работает быстро. Playwright кросс-браузерный, поддерживает эмуляцию устройств и interception сетевых запросов.
- **Архитектурные паттерны:** Test Pyramid, Mocking External Services (Mailgun, S3), Page Object Model (E2E), Arrange-Act-Assert (AAA).

**ESLint + Biome + Ruff + Pytest**
- **Назначение:** Линтинг, форматирование и тестирование для JS/TS и Python.
- **Обоснование:** Biome заменяет ESLint/Prettier с высокой производительностью. Ruff — ultrafast Python linter. Pytest — стандарт де-факто для Python тестов.
- **Архитектурные паттерны:** Pre-commit Hooks, Fail-Fast CI Gates, Consistent Style Enforcement, Isolated Test Environments.

---

## ⚙️ Backend & API

**FastAPI + Uvicorn**
- **Назначение:** Асинхронный веб-фреймворк и ASGI-сервер.
- **Обоснование:** Автоматическая генерация OpenAPI/Swagger, высокая производительность (Starlette + Pydantic), встроенная валидация данных.
- **Архитектурные паттерны:** Clean Architecture / Layered Architecture, Dependency Injection, Async-First Design, DTO Pattern.

**uv (workspace)**
- **Назначение:** Современный менеджер Python-пакетов и проектов.
- **Обоснование:** На порядки быстрее `pip`/`poetry`, поддерживает workspace-зависимости и lockfile-based reproducibility.
- **Архитектурные паттерны:** Deterministic Builds, Virtual Environment Isolation, Workspace Dependency Resolution.

---

## 📬 Task Queue & Messaging (Production Config)

**RabbitMQ + Celery + Mailgun**
- **Назначение:** Брокер сообщений, маршрутизация, асинхронный обработчик задач (`rpc://` result backend) и отправка email-уведомлений.
- **Обоснование:** RabbitMQ гарантирует доставку. Celery управляет роутингом и retry-логикой. Mailgun обеспечивает высокую deliverability с встроенными DKIM/SPF и webhook-отчетами о доставке/открытиях.
- **Архитектурные паттерны (Startup-Defaults):** 
  - At-Least-Once Delivery + Idempotent Task Design
  - `rpc://` Result Backend с `result_expires=3600`
  - `worker_prefetch_multiplier=4`, `worker_max_tasks_per_child=1000`
  - **MVP Task Routing:**
    - `emails`: High-priority queue, Mailgun HTTP API, rate-limit (10/s), retry on 5xx, DLX on hard-bounce.
    - `reports`: Default queue, `task_time_limit=300`, progress broadcasting via WS hooks.
    - `files`: Low-priority queue, chunked processing, auto-cleanup on completion/failure.
  - Dead-Letter Exchange (DLX) для отлова failed-задач

---

## 📁 Storage & File Management

**S3-Compatible Storage (MinIO for Dev / AWS/Selectel for Prod)**
- **Назначение:** Надежное хранение пользовательских файлов, сгенерированных отчетов и медиа-ресурсов.
- **Обоснование:** Объектное хранилище масштабируется независимо от VPS-диска. Presigned URLs позволяют загружать/скачивать файлы напрямую с клиента, снимая нагрузку с бэкенда.
- **Архитектурные паттерны:** 
  - Presigned URL Upload/Download (Zero-backend bandwidth)
  - Object Lifecycle Policies (auto-delete temp files, archive reports after 90 days)
  - Bucket-per-tenant or Prefix-isolation for multi-user separation
  - Async `aioboto3` for non-blocking backend operations

---

## 🗄️ Database & Migrations

**PostgreSQL**
- **Назначение:** Основная реляционная СУБД для бизнес-данных.
- **Обоснование:** ACID-совместимость, поддержка JSONB, полнотекстовый поиск. Отделена от брокера сообщений и объектного хранилища.
- **Архитектурные паттерны:** Connection Pooling (asyncpg), Row-Level Security, JSONB for Semi-structured Data. *(На старте достаточно встроенного пула)*

**Alembic**
- **Назначение:** Управление миграциями БД.
- **Обоснование:** Интегрируется с SQLAlchemy, версионирует схему, поддерживает rollback и авто-генерацию миграций.
- **Архитектурные паттерны:** Declarative Migrations, Schema Version Control, Idempotent Rollback Strategy, Zero-Downtime Migrations.

---

## 📊 Observability

**OpenTelemetry Web SDK + Sentry**
- **Назначение:** Трассировка frontend-запросов, сбор ошибок и метрик производительности.
- **Обоснование:** OTel обеспечивает vendor-agnostic телеметрию. Sentry дает детальные отчеты об ошибках с интеграцией source maps.
- **Архитектурные паттерны:** Distributed Tracing (W3C TraceContext), Error Boundaries, Context Propagation, Sampling Strategies.

**Prometheus + Grafana**
- **Назначение:** Сбор метрик и визуализация дашбордов.
- **Обоснование:** Prometheus — стандарт для pull-based метрик. Интегрируется с `rabbitmq-prometheus` и `celery-exporter`.
- **Архитектурные паттерны:** RED/USE Method, Dashboard-as-Code, Alerting Rules with Runbooks, Metric Cardinality Control. *(Фокус: Error Rate, Queue Depth, WS Active Connections, S3 Upload Latency, Mailgun Delivery Rate)*

---

## 🚀 CI/CD & Infrastructure (Docker Swarm Optimized)

**GitHub Actions → Docker Swarm Deploy**
- **Назначение:** Автоматизация сборки, тестирования и rolling-деплоя в production-кластер.
- **Обоснование:** GitHub Actions собирает образы, публикует в registry (GHCR/Docker Hub). Swarm принимает стек через `docker stack deploy`, управляя репликами, secrets и overlay-сетями.
- **Архитектурные паттерны:** Trunk-Based Development, Pipeline-as-Code, Multi-arch Builds, Immutable Infrastructure.

**Traefik v3 + Docker Swarm**
- **Назначение:** Reverse-proxy, load-balancer и автоматический SSL-менеджер для `mydomain.ru`.
- **Обоснование:** Нативная интеграция со Swarm через Docker labels. Автоматически маршрутизирует трафик, обновляет SSL (Let's Encrypt), поддерживает WebSocket upgrade и HTTP/2.
- **Архитектурные паттерны:** 
  - Overlay Network Isolation (`frontend`, `backend`, `database`)
  - Docker Secrets for Mailgun API Keys, DB Credentials, S3 Keys
  - Rolling Updates (`update_config: parallelism: 1, delay: 10s`)
  - Healthchecks & Readiness Probes for zero-downtime deploys
  - Resource Constraints (`mem_limit`, `cpu_limit`, `reservation`)

---

## 📐 Self-Review & Next Steps

### 🔍 Критический анализ рисков (Production/VPS Swarm Context)
1. **Swarm Learning Curve & State:** Docker Swarm проще K8s, но не имеет встроенного auto-scaling или complex service mesh. Для стартапа это плюс (меньше overhead), но при резком росте >50k DAU потребуется миграция на K8s. Решение: абстрагировать deploy-скрипты, хранить state externally.
2. **S3 Lifecycle & Cost:** Хранение отчетов и файлов без правил приведет к росту затрат. Решение: явные `lifecycle_configuration` (удаление черновиков через 24ч, архивация отчетов через 90д, transition to Glacier).
3. **Mailgun Deliverability & Webhooks:** Самоподписанные домены без DNS-записей попадут в спам. Решение: настроить SPF/DKIM/DMARC для `mydomain.ru`, включить Mailgun webhooks в Celery для отслеживания `delivered`, `bounced`, `complained`.

### 📈 Приоритизация реализации (MVP → Production)
1. **Фаза 1 (Foundation):** `turbo.json`, Docker Compose (local dev), GitHub Actions build/test, линтеры, auth flow.
2. **Фаза 2 (Core API & DB):** FastAPI endpoints, Alembic init, `openapi-typescript` → Zod → Nuxt UI, S3 presigned URLs flow.
3. **Фаза 3 (Async & Real-time):** Celery workers (`rpc://`), RabbitMQ queues, Mailgun integration, FastAPI WS + Nuxt client, status broadcasting.
4. **Фаза 4 (Swarm & Prod Deploy):** Traefik config, Docker Swarm init, `docker-compose.yml` → `docker-stack.yml`, secrets management, SSL for `mydomain.ru`, CORS/Cookie hardening.
5. **Фаза 5 (Hardening & Observability):** Sentry, Prometheus + Grafana, Playwright E2E, S3 lifecycle policies, Mailgun webhook handlers, load testing.

### ❓ Адаптивные вопросы для следующей итерации
1. Какой S3-провайдер предпочтителен для продакшна (AWS S3, Selectel Cloud, Yandex Object Storage, MinIO on-prem)? Это повлияет на `endpoint_url`, `region` и `boto3` конфигурацию.
2. Требуется ли CDN (Cloudflare/Selectel CDN) для статики Nuxt и публичных файлов из S3, или достаточно прямых запросов к `mydomain.ru` + кэширования Traefik?
3. Нужен ли отдельный домен/субдомен для API (`api.mydomain.ru`) или всё будет на `mydomain.ru` с path-based routing (`/api/*`, `/ws/*`, `/*`)?
