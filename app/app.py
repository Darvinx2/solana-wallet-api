from flask import Flask

from api.portfolio import bp as bp_get_portfolio
from app.container import build_services
from app.extensions import db, migrate, settings
from services.wallet_portfolio_service import WalletPortfolioService
from utils.logger import setup_logger


class App(Flask):
    portfolio_service: WalletPortfolioService


def create_app() -> App:
    app = App(__name__)

    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)

    setup_logger(app)

    services = build_services()
    app.portfolio_service = services["portfolio_service"]

    app.register_blueprint(bp_get_portfolio)

    return app
