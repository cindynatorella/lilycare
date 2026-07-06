from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class DatabaseConfig:
    """Store the settings needed to connect to PostgreSQL."""

    host: str = "localhost"
    port: int = 5432
    database: str = "lilycare_db"
    user: str = "lilycare_user"
    password: str = "lilycare"
    sslmode: str = "prefer"


# Read PostgreSQL settings from environment variables so secrets stay out of code.
def load_database_config() -> DatabaseConfig:
	defaults = DatabaseConfig()

	return DatabaseConfig(
		host=os.getenv("LILYCARE_DB_HOST") or defaults.host,
		port=int(os.getenv("LILYCARE_DB_PORT") or defaults.port),
		database=os.getenv("LILYCARE_DB_NAME") or defaults.database,
		user=os.getenv("LILYCARE_DB_USER") or defaults.user,
		password=os.getenv("LILYCARE_DB_PASSWORD") or defaults.password,
		sslmode=os.getenv("LILYCARE_DB_SSLMODE") or defaults.sslmode,
	)
