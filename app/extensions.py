from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from httpx import Client

from app.config import Config

db = SQLAlchemy()
settings = Config()
migrate = Migrate()
httpx_client = Client()
