from __future__ import annotations

from typing import Any

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # pragma: no cover - dependency may not be installed yet
    psycopg = None
    dict_row = None

from .config import DatabaseConfig, load_database_config


# Create and return a PostgreSQL connection using the loaded app config.
def get_connection(config: DatabaseConfig | None = None) -> Any:
    if psycopg is None:
        raise RuntimeError("psycopg is not installed yet. Add backend dependencies first.")

    config = config or load_database_config()
    return psycopg.connect(
        host=config.host,
        port=config.port,
        dbname=config.database,
        user=config.user,
        password=config.password,
        sslmode=config.sslmode,
        row_factory=dict_row,
    )


# Open a connection and run a very small query to confirm PostgreSQL is reachable.
def test_connection(config: DatabaseConfig | None = None) -> bool:
    raise NotImplementedError("TODO: Open a connection and return True when `SELECT 1` succeeds.")


# Read the schema file and create the app tables in PostgreSQL.
def initialize_database(config: DatabaseConfig | None = None) -> None:
    raise NotImplementedError("TODO: Execute the SQL in backend/schema.sql against the database.")
