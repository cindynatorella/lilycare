from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, text

from .config import DatabaseConfig, load_database_config


db = SQLAlchemy()


def build_database_url(config: DatabaseConfig | None = None) -> str:
	config = load_database_config() or config

	url = URL.create(
		drivername="postgresql+psycopg",
		username=config.user,
		password=config.password,
		host=config.host,
		port=config.port,
		database=config.database,
		query={"sslmode": config.sslmode},
	)

	return url.render_as_string(hide_password=False)


def configure_database(app, config: DatabaseConfig | None = None) -> None:
	app.config["SQLALCHEMY_DATABASE_URI"] = build_database_url(config)
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db.init_app(app)


def test_connection(app) -> bool:
	with app.app_context():
		db.session.execute(text("SELECT 1"))

	return True