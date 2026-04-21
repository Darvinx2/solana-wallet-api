import bcrypt
from flask_jwt_extended import create_access_token

from models.models import User
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, login: str, password: str) -> dict:
        if self.user_repo.get_user_by_login(login):
            return {"error": "User already exists"}

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = self.user_repo.create_user(login, password_hash)
        return {"user_id": user.id, "login": user.login}

    def login(self, login: str, password: str) -> dict:
        user = self.user_repo.get_user_by_login(login)
        if not user:
            return {"error": "Invalid credentials"}

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return {"error": "Invalid credentials"}

        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}
