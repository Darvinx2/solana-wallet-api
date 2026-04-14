from flask import Flask

from app.extensions import db, migrate, settings


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(settings)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate.init_app(app, db)

    return app
