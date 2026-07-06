"""Backend package for LilyCare's future PostgreSQL integration."""

from .config import DatabaseConfig, load_database_config
from .db import configure_database, db

