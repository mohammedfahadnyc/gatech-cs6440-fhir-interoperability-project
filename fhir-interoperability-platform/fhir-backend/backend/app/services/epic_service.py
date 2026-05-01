from urllib.parse import urlencode

import requests
from flask import current_app
from itsdangerous import BadSignature, URLSafeSerializer

from app.models.patient_model import Patient
from app.models.user_model import User


STATE_SALT = "epic-oauth-state"


def _serializer():
    return URLSafeSerializer(current_app.config["SECRET_KEY"], salt=STATE_SALT)


def _auth_base_url():
    return current_app.config["EPIC_AUTH_BASE_URL"].rstrip("/")


def _require_epic_config():
    if not current_app.config.get("EPIC_ENABLED"):
        raise ValueError("Epic sandbox integration is disabled")

    missing = [
        key
        for key in ("EPIC_CLIENT_ID", "EPIC_CLIENT_SECRET", "EPIC_REDIRECT_URI")
        if not current_app.config.get(key)
    ]
    if missing:
        raise ValueError(f"Missing Epic configuration: {', '.join(missing)}")


def is_epic_demo_patient(user, patient):
    configured = current_app.config.get("EPIC_DEMO_PATIENT_EMAILS") or ""
    allowed_emails = {
        email.strip().lower()
        for email in configured.split(",")
        if email.strip()
    }
    return (
        user.role == "patient"
        and user.email.lower() in allowed_emails
        and user.patient_id == patient.id
    )


def build_epic_authorization_url(user, patient):
    _require_epic_config()

    state = _serializer().dumps(
        {"user_id": user.id, "patient_id": patient.id, "source": "epic"}
    )
    params = {
        "client_id": current_app.config["EPIC_CLIENT_ID"],
        "response_type": "code",
        "redirect_uri": current_app.config["EPIC_REDIRECT_URI"],
        "aud": current_app.config["EPIC_FHIR_BASE_URL"],
        "scope": "openid fhirUser",
        "state": state,
    }
    return f"{_auth_base_url()}/oauth2/authorize?{urlencode(params)}"


def exchange_epic_code_for_token(code):
    _require_epic_config()

    token_url = f"{_auth_base_url()}/oauth2/token"
    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": current_app.config["EPIC_REDIRECT_URI"],
        },
        auth=(
            current_app.config["EPIC_CLIENT_ID"],
            current_app.config["EPIC_CLIENT_SECRET"],
        ),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def consume_epic_callback(code, state):
    if not code or not state:
        raise ValueError("Missing Epic authorization code or state")

    try:
        payload = _serializer().loads(state)
    except BadSignature as exc:
        raise ValueError("Invalid Epic authorization state") from exc

    user = User.query.get_or_404(payload["user_id"])
    patient = Patient.query.get_or_404(payload["patient_id"])
    if not is_epic_demo_patient(user, patient):
        raise ValueError("Epic sandbox authorization is only enabled for External Patient C and External Patient B")

    token_payload = exchange_epic_code_for_token(code)
    patient.is_authorized = True
    patient.is_imported = False
    patient.data_source = "epic"

    return {
        "patient": patient,
        "token_payload": token_payload,
    }
