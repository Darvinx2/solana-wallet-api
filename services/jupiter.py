import logging
from typing import List

from httpx import Client, ConnectError, HTTPError

from schemas.token import Token
from services.base import BaseApiClient

logger = logging.getLogger(__name__)


class JupiterPrice(BaseApiClient):
    BASE_URL = "https://lite-api.jup.ag/tokens/v2/"

    def __init__(self, session: Client, token: List[Token]):
        self.session = session
        self.token = token

    async def tokens_info(self) -> List[Token]:
        tokens = []
        for info in self.token:
            url = f"{self.BASE_URL}search?query={str(info.address)}"
            try:
                r = self.session.get(url)
                data = self.handler_response(r, "JupiterAPI")
                if len(data) < 1:
                    logger.warning("Error: empty array received")
                    continue
                else:
                    for token in data:
                        price = token.get("usdPrice")
                        if price is None:
                            logger.error(f"Price {info.name} is None")
                        else:
                            tokens.append(
                                Token(
                                    name=info.name,
                                    balance=info.balance,
                                    price=price,
                                )
                            )
            except ConnectError as e:
                logger.error(f"Не удалось подключиться к JupiterAPI: {e}")
                raise Exception(
                    "Не удалось подключиться к JupiterAPI, проверьте подключение к интернету"
                )
            except HTTPError as e:
                logger.error(f"Не удалось подключиться к JupiterAPI: {e}")
                raise Exception("JupiterAPI не отвечает")

        return tokens
