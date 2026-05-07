import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import settings

# Alembic Config — даёт доступ к alembic.ini
config = context.config

# Настройка логирования из alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL из pydantic-settings, не из alembic.ini
# ref: spec.md → PostgreSQL, asyncpg
config.set_main_option("sqlalchemy.url", settings.database_url)

# Импортируем Base со всеми моделями для автогенерации миграций.
# Добавляйте импорты моделей по мере их создания:
#   from app.models.user import User  # noqa: F401
try:
    from app.db.base import Base  # noqa: F401
    target_metadata = Base.metadata
except ImportError:
    target_metadata = None


def run_migrations_offline() -> None:
    """Миграции без подключения к БД (генерация SQL-скрипта)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Миграции через async engine (asyncpg). ref: spec.md → asyncpg"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
