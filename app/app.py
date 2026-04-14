from flask import Flask

from app.extensions import db, migrate, settings
from utils.logger import setup_logger


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)

    setup_logger(app)

    return app
