from typing import TYPE_CHECKING, cast

from flask import Blueprint, current_app, jsonify, request

if TYPE_CHECKING:
    from app.app import App

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/register")
def register():
    app = cast("App", current_app)
    body = request.get_json(silent=True) or {}
    login = body.get("login")
    password = body.get("password")

    if not login or not password:
        return jsonify({"error": "login and password are required"}), 400

    result = app.auth_service.register(login, password)
    if "error" in result:
        return jsonify(result), 409

    return jsonify(result), 201


@bp.post("/login")
def login():
    app = cast("App", current_app)
    body = request.get_json(silent=True) or {}
    login = body.get("login")
    password = body.get("password")

    if not login or not password:
        return jsonify({"error": "login and password are required"}), 400

    result = app.auth_service.login(login, password)
    if "error" in result:
        return jsonify(result), 401

    return jsonify(result), 200
