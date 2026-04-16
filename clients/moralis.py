import logging
from typing import Any, Mapping

from httpx import Client, ConnectError, HTTPError

from app.extensions import settings
from clients.base import BaseApiClient
from schemas.token import Token

logger = logging.getLogger(__name__)


class MoralisPortfolio(BaseApiClient):
    BASE_URL = "https://solana-gateway.moralis.io/account/mainnet/"

    def __init__(self, session: Client) -> None:
        self.session = session
        self._headers = {"Accept": "application/json", "X-API-Key": settings.MORALIS_API_TOKEN}

    def get_portfolio(self, wallet: str) -> Mapping[str, Any]:
        url = f"{self.BASE_URL}{wallet}/portfolio"
        params = {
            "nftMetadata": "false",
            "mediaItems": "false",
            "excludeSpam": "true",
        }

        try:
            r = self.session.get(url, headers=self._headers, params=params)
            return self.handler_response(r, "MoralisAPI")
        except ConnectError as e:
            logger.error(f"Не удалось подключиться к MoralisAPI: {e}")
            raise Exception(
                "Не удалось подключиться к MoralisAPI, проверьте подключение к интернету"
            )
        except HTTPError as e:
            logger.error(f"Не удалось подключиться к MoralisAPI: {e}")
            raise Exception("MoralisAPI не отвечает")

    def get_tokens(self, wallet: str) -> list[Token]:
        data = self.get_portfolio(wallet)
        solana_address = "So11111111111111111111111111111111111111112"
        solana_balance = str(data.get("nativeBalance", {}).get("solana", "0"))
        solana = Token(
            name="Solana",
            balance=solana_balance,
            address=solana_address,
        )
        tokens = [
            Token(
                name=token.get("name"),
                balance=token.get("amount"),
                address=token.get("mint"),
            )
            for token in data.get("tokens", [])
        ]
        tokens.append(solana)
        return tokens
