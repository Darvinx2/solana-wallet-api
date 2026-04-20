import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask, g, request


def setup_logger(app: Flask):
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=10_000_000,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    @app.before_request
    def before():
        g.start_time = time.time()

    @app.after_request
    def after(response):
        duration = time.time() - g.start_time
        app.logger.info(
            f"{request.method} {request.path} "
            f"-> {response.status_code} "
            f"({duration:.3f}s)"
        )
        return response
