from typing import cast, TYPE_CHECKING

from flask import Blueprint, current_app, jsonify, request

if TYPE_CHECKING:
    from app.app import App

bp = Blueprint("farm", __name__, url_prefix="/farm")


@bp.post("/")
def create_farm():
    app = cast("App", current_app)
    body = request.get_json(silent=True) or {}
    user_id = body.get("user_id")
    wallet_addresses = body.get("wallets", [])

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    result = app.farm_service.create_farm(user_id, wallet_addresses)
    return jsonify(result), 201


@bp.get("/user/<int:user_id>")
def get_user_farms(user_id: int):
    app = cast("App", current_app)
    farms = app.farm_service.repo.get_farms_by_user(user_id)
    return jsonify([{"farm_id": f.id, "total_usd": float(f.total_usd), "date": f.date.isoformat()} for f in farms])


@bp.get("/<int:farm_id>")
def check_farm(farm_id: int):
    app = cast("App", current_app)
    result = app.farm_service.check_farm(farm_id)
    return jsonify(result)


@bp.delete("/<int:farm_id>")
def delete_farm(farm_id: int):
    app = cast("App", current_app)
    app.farm_service.repo.delete_farm(farm_id)
    return jsonify({"deleted": farm_id})
