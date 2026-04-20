from typing import cast, TYPE_CHECKING

from flask import Blueprint, current_app, jsonify


bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@bp.get("/<wallet_address>")
def get_portfolio(wallet_address: str):
    app = cast("App", current_app)
    result = app.portfolio_service.build_portfolio(wallet_address)
    return jsonify(result)
