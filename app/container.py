from app.extensions import httpx_client
from clients.jupiter import JupiterPrice
from clients.moralis import MoralisPortfolio
from services.wallet_portfolio_service import WalletPortfolioService


def build_services() -> dict:
    moralis = MoralisPortfolio(httpx_client)
    jupiter = JupiterPrice(httpx_client)

    return {
        "portfolio_service": WalletPortfolioService(moralis, jupiter),
    }
