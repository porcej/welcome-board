from __future__ import with_statement
import os
from logging.config import fileConfig
import os as _os
from sqlalchemy import engine_from_config, pool
from alembic import context
from flask import current_app

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging if it exists.
# Flask-Migrate may not provide a physical alembic.ini alongside migrations.
if config.config_file_name is not None and _os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)

# target metadata from Flask-Migrate's db
target_metadata = current_app.extensions["migrate"].db.metadata


def run_migrations_offline():
    url = os.getenv("DATABASE_URL") or current_app.config["SQLALCHEMY_DATABASE_URI"]
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Reuse the application's engine instead of creating a new one
    connectable = current_app.extensions["migrate"].db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


