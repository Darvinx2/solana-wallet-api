from sqlalchemy import select

from app.extensions import db
from models.models import User


class UserRepository:
    @staticmethod
    def get_user(user_id: int) -> User | None:
        return db.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
