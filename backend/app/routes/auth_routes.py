from flask import Blueprint, jsonify, request

from app.middleware.rbac import get_current_user, role_required
from app.services.auth_service import authenticate_user, build_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"token": build_token(user), "user": user.to_dict()})


@auth_bp.route("/me", methods=["GET"])
@role_required("clinician", "admin", "patient")
def me():
    return jsonify(get_current_user().to_dict())
