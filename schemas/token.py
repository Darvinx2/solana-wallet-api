from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    name: str = ""
    balance: float = 0
    address: Optional[str] = None
    price: Optional[float] = None

    @property
    def total_amount(self) -> Optional[float]:
        if self.price is None:
            return None
        total = round(self.price * self.balance, 2)
        return total if total > 1 else None
