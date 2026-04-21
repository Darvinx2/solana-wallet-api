from sqlalchemy import select

from app.extensions import db
from models.models import User


class UserRepository:
    @staticmethod
    def get_user(user_id: int) -> User | None:
        return db.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    @staticmethod
    def get_user_by_login(login: str) -> User | None:
        return db.session.execute(select(User).where(User.login == login)).scalar_one_or_none()

    @staticmethod
    def create_user(login: str, password_hash: str) -> User:
        user = User(login=login, password=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
