from clients.jupiter import JupiterPrice
from clients.moralis import MoralisPortfolio
from schemas.token import Token


class WalletPortfolioService:
    def __init__(self, moralis: MoralisPortfolio, jupiter: JupiterPrice):
        self.moralis = moralis
        self.jupiter = jupiter

    def build_portfolio(self, wallet_address: str) -> dict:
        tokens = self._get_tokens(wallet_address)
        priced_tokens = self._enrich_with_prices(tokens)
        total_usd = self._calculate_total(priced_tokens)

        return {
            "wallet_address": wallet_address,
            "tokens": [t.model_dump() for t in priced_tokens],
            "total_usd": total_usd,
        }

    def _get_tokens(self, wallet_address: str) -> list[Token]:
        return self.moralis.get_tokens(wallet_address)

    def _enrich_with_prices(self, tokens: list[Token]) -> list[Token]:
        return self.jupiter.tokens_info(tokens)

    @staticmethod
    def _calculate_total(tokens: list[Token]) -> float:
        return sum(token.total_amount or 0 for token in tokens)
