from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from app.models.user_model import User


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            # Claims are attached at login so role checks stay fast and consistent.
            if claims.get("role") not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def get_current_user():
    verify_jwt_in_request()
    user_id = int(get_jwt_identity())
    return User.query.get_or_404(user_id)


def patient_scope_required(patient_id):
    user = get_current_user()
    # Clinicians and admins have full visibility; patients stay restricted to their own chart.
    if user.role in {"clinician", "admin"}:
        return None
    if user.role == "patient" and user.patient_id == patient_id:
        return None
    return jsonify({"error": "Forbidden"}), 403
