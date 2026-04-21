from pydantic_settings import BaseSettings


class Config(BaseSettings):
    FLASK_APP: str
    SQLALCHEMY_DATABASE_URI: str
    MORALIS_API_TOKEN: str
    JWT_SECRET_KEY: str
    JWT_TOKEN_LOCATION: list[str] = ["headers", "cookies"]

    model_config = {"env_file": ".env", "extra": "ignore"}
