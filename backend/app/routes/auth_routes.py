from flask import Blueprint, jsonify, request

from app.middleware.rbac import get_current_user, role_required
from app.services.auth_service import authenticate_user, build_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and return a JWT.
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: doctor1@clinic.com
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login succeeded
      400:
        description: Missing email or password
      401:
        description: Invalid credentials
    """
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
    """
    Get the currently authenticated user.
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Current user profile
      401:
        description: Missing or invalid token
      403:
        description: Forbidden
    """
    return jsonify(get_current_user().to_dict())
