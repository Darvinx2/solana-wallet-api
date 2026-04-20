from sqlalchemy import select

from models.models import Farm, Wallet
from app.extensions import db


class FarmRepository:
    @staticmethod
    def get_farm(farm_id: int) -> Farm | None:
        return db.session.execute(select(Farm).where(Farm.id == farm_id)).scalar_one_or_none()

    @staticmethod
    def get_farms_by_user(user_id: int) -> list[Farm]:
        return list(db.session.execute(select(Farm).where(Farm.user_id == user_id)).scalars())

    def delete_farm(self, farm_id: int):
        farm = self.get_farm(farm_id)
        if farm:
            db.session.delete(farm)
            db.session.commit()

    def get_wallet_addresses_by_farm(self, farm_id: int) -> list[str]:
        farm = self.get_farm(farm_id)
        if not farm:
            return []
        return [w.address for w in farm.wallet]

    @staticmethod
    def create_farm(user_id: int, total_usd: float) -> Farm:
        farm = Farm(user_id=user_id, total_usd=total_usd)
        db.session.add(farm)
        db.session.commit()
        return farm

    @staticmethod
    def add_wallet(farm_id: int, address: str) -> Wallet:
        wallet = Wallet(farm_id=farm_id, address=address)
        db.session.add(wallet)
        db.session.commit()
        return wallet
