from typing import cast, TYPE_CHECKING

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

if TYPE_CHECKING:
    from app.app import App

bp = Blueprint("farm", __name__, url_prefix="/farm")


@bp.post("/")
@jwt_required()
def create_farm():
    app = cast("App", current_app)
    user_id = int(get_jwt_identity())
    body = request.get_json(silent=True) or {}
    wallet_addresses = body.get("wallets", [])

    result = app.farm_service.create_farm(user_id, wallet_addresses)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 201


@bp.get("/")
@jwt_required()
def get_user_farms():
    app = cast("App", current_app)
    user_id = int(get_jwt_identity())
    farms = app.farm_service.repo.get_farms_by_user(user_id)
    return jsonify([{"farm_id": f.id, "total_usd": float(f.total_usd), "date": f.date.isoformat()} for f in farms])


@bp.get("/<int:farm_id>")
@jwt_required()
def check_farm(farm_id: int):
    app = cast("App", current_app)
    result = app.farm_service.check_farm(farm_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)


@bp.delete("/<int:farm_id>")
@jwt_required()
def delete_farm(farm_id: int):
    app = cast("App", current_app)
    app.farm_service.repo.delete_farm(farm_id)
    return jsonify({"deleted": farm_id})
