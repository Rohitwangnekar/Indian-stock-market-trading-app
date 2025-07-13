from finance import app, db, migrate
from alembic import command
from alembic.config import Config

with app.app_context():
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", migrate.directory)
    # Set the SQLAlchemy URL from the Flask app's config
    alembic_cfg.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])
    command.upgrade(alembic_cfg, "head")