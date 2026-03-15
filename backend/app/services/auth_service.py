from flask_jwt_extended import create_access_token

from app.models.user_model import User


def authenticate_user(email, password):
    user = User.query.filter_by(email=email.lower()).first()
    if not user or not user.check_password(password):
        return None
    return user


def build_token(user):
    additional_claims = {"role": user.role, "patient_id": user.patient_id}
    return create_access_token(identity=str(user.id), additional_claims=additional_claims)
