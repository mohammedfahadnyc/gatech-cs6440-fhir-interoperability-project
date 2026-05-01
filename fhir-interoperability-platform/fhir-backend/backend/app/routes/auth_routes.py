from urllib.parse import urlencode

from flask import Blueprint, current_app, jsonify, redirect, request

from app.db.database import db
from app.middleware.rbac import get_current_user, role_required
from app.services.auth_service import authenticate_user, build_token
from app.services.epic_service import consume_epic_callback

auth_bp = Blueprint("auth", __name__)


def _frontend_redirect(path="", **params):
    frontend_url = (current_app.config.get("FRONTEND_APP_URL") or "").rstrip("/")
    if not frontend_url:
        return None

    destination = frontend_url
    if path:
        destination = f"{frontend_url}/{path.lstrip('/')}"
    if params:
        destination = f"{destination}?{urlencode(params)}"
    return redirect(destination)


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
              example: clinician.demo1@example.local
            password:
              type: string
              example: local-demo-password
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


@auth_bp.route("/epic/callback", methods=["GET"])
def epic_callback():
    """
    Complete the Epic sandbox OAuth callback for the External Patient C demo flow.
    ---
    tags:
      - Auth
    parameters:
      - in: query
        name: code
        type: string
      - in: query
        name: state
        type: string
      - in: query
        name: error
        type: string
    responses:
      200:
        description: Epic authorization completed
      400:
        description: Invalid callback or declined authorization
    """
    if request.args.get("error"):
        error = request.args.get("error")
        description = request.args.get("error_description") or "Epic authorization was declined"
        redirect_response = _frontend_redirect(
            "",
            epic="error",
            message=description,
        )
        if redirect_response:
            return redirect_response
        return jsonify({"error": error, "message": description}), 400

    try:
        result = consume_epic_callback(
            request.args.get("code"),
            request.args.get("state"),
        )
    except Exception as exc:
        redirect_response = _frontend_redirect(
            "",
            epic="error",
            message=str(exc),
        )
        if redirect_response:
            return redirect_response
        return jsonify({"error": str(exc)}), 400

    db.session.commit()
    patient = result["patient"]
    redirect_response = _frontend_redirect(
        "",
        epic="success",
        patient_id=patient.id,
        source="epic",
    )
    if redirect_response:
        return redirect_response
    return jsonify(
        {
            "message": "Epic sandbox authorization completed successfully",
            "patient": patient.to_dict(),
            "epic_patient_id": result["token_payload"].get("patient"),
        }
    )
