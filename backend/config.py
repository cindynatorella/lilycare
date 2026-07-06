from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class DatabaseConfig:
    """Store the settings needed to connect to PostgreSQL."""

    host: str
    port: int
    database: str
    user: str
    password: str
    sslmode: str = "prefer"


# Read PostgreSQL settings from environment variables so secrets stay out of code.
def load_database_config() -> DatabaseConfig:
    return DatabaseConfig(
        host=os.getenv("LILYCARE_DB_HOST", "localhost"),
        port=int(os.getenv("LILYCARE_DB_PORT", "5432")),
        database=os.getenv("LILYCARE_DB_NAME", "lilycare"),
        user=os.getenv("LILYCARE_DB_USER", "postgres"),
        password=os.getenv("LILYCARE_DB_PASSWORD", ""),
        sslmode=os.getenv("LILYCARE_DB_SSLMODE", "prefer"),
    )
