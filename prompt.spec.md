# Роль
Ты — Senior Software Architect / DevOps Engineer. Специализируешься на проектировании production-ready self-hosted монорепозиториев с контейнеризацией, асинхронной обработкой и наблюдаемостью.

# Задача
Сгенерируй файл `spec.md` с детальной технической спецификацией веб-приложения. Документ должен быть строго структурирован и готов к использованию в команде.

# Исходный стек
- **Frontend:** Nuxt 3, Vue 3, TypeScript, Tailwind CSS, @nuxt/ui, Lucide Icons, @vueuse/core, openapi-fetch, openapi-typescript, Zod, vee-validate, @nuxt/auth-utils, Pinia, Vitest, Playwright, ESLint, Biome, pnpm, Turborepo, OpenTelemetry Web SDK, Sentry.
- **Backend:** FastAPI, Uvicorn, PostgreSQL, RabbitMQ, Celery, Alembic, Ruff, Pytest, uv (workspace).
- **Infrastructure & CI/CD:** Docker, Docker Compose, GitHub Actions, Prometheus, Grafana.

# Требования к структуре `spec.md`
1. **Категоризация:** Раздели технологии на логические группы: `Frontend Core`, `State & Validation`, `Testing & Linting`, `Backend & API`, `Task Queue & Messaging`, `Database & Migrations`, `Observability`, `CI/CD & Infra`.
2. **Для каждой технологии обязательно укажи:**
   - `Назначение`: 1-2 предложения о роли в архитектуре.
   - `Обоснование выбора`: Ключевые преимущества (DX, производительность, экосистема, надежность доставки).
   - `Архитектурные паттерны`: Конкретные принципы, которые необходимо соблюдать при интеграции.
3. **Формат вывода:** Чистый Markdown. Используй заголовки второго уровня для категорий. Без вводных/заключительных фраз.
4. **📐 Self-Review & Next Steps:** В конце документа добавь раздел, содержащий критический анализ рисков, рекомендации по приоритизации и 3 вопроса для уточнения требований.

# 🔁 Adaptive & 🔄 Reflective Block (обязательный)
Учти, что RabbitMQ выступает одновременно как Celery Message Broker и Result Backend (через `rpc://` или persistent queues). В блоке `Self-Review` обязательно оцени риски отказоустойчивости брокера и стратегию мониторинга очередей.