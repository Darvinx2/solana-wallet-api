from repositories.farm_repository import FarmRepository
from repositories.user_repository import UserRepository
from services.wallet_portfolio_service import WalletPortfolioService
from utils.solana import is_valid_solana_address


class FarmService:
    def __init__(self, repo: FarmRepository, user_repo: UserRepository, portfolio: WalletPortfolioService):
        self.repo = repo
        self.user_repo = user_repo
        self.portfolio = portfolio

    def create_farm(self, user_id: int, wallet_addresses: list[str]) -> dict:
        if not self.user_repo.get_user(user_id):
            return {"error": f"User {user_id} not found"}

        valid = [address for address in wallet_addresses if is_valid_solana_address(address)]
        if not valid:
            return {"error": "No valid Solana addresses provided"}

        portfolios = [self.portfolio.build_portfolio(addr) for addr in valid]
        total_usd = sum(p["total_usd"] for p in portfolios)

        farm = self.repo.create_farm(user_id, total_usd)
        for addr in valid:
            self.repo.add_wallet(farm.id, addr)

        return {"farm_id": farm.id, "wallets_added": len(valid), "total_usd": total_usd}

    def check_farm(self, farm_id: int) -> dict:
        addresses = self.repo.get_wallet_addresses_by_farm(farm_id)
        if not addresses:
            return {"error": "Farm not found or empty"}

        wallets = [self.portfolio.build_portfolio(addr) for addr in addresses]
        total_usd = sum(w["total_usd"] for w in wallets)

        return {"farm_id": farm_id, "total_usd": total_usd, "wallets": wallets}
