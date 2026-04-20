from flask import Flask

from api.farm import bp as bp_farm
from api.portfolio import bp as bp_get_portfolio
from app.extensions import db, httpx_client, migrate, settings
from clients.jupiter import JupiterPrice
from clients.moralis import MoralisPortfolio
from repositories.farm_repository import FarmRepository
from repositories.user_repository import UserRepository
from services.farm_service import FarmService
from services.wallet_portfolio_service import WalletPortfolioService
from utils.logger import setup_logger


class App(Flask):
    portfolio_service: WalletPortfolioService
    farm_service: FarmService


def create_app() -> App:
    app = App(__name__)

    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)

    setup_logger(app)

    portfolio_service = WalletPortfolioService(MoralisPortfolio(httpx_client), JupiterPrice(httpx_client))
    app.portfolio_service = portfolio_service
    app.farm_service = FarmService(FarmRepository(), UserRepository(), portfolio_service)

    app.register_blueprint(bp_get_portfolio)
    app.register_blueprint(bp_farm)

    return app
