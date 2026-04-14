from pydantic_settings import BaseSettings


class Config(BaseSettings):
    FLASK_APP: str
    SQLALCHEMY_DATABASE_URI: str

    model_config = {"env_file": ".env"}
