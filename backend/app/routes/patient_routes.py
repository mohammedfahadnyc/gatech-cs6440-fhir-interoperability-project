from flask import Blueprint, jsonify

from app.middleware.rbac import get_current_user, role_required
from app.models.patient_model import Patient

patient_bp = Blueprint("patients", __name__)


@patient_bp.route("", methods=["GET"])
@role_required("clinician", "admin")
def list_patients():
    patients = Patient.query.order_by(Patient.name.asc()).all()
    return jsonify([patient.to_dict() for patient in patients])


@patient_bp.route("/<int:patient_id>", methods=["GET"])
@role_required("clinician", "admin", "patient")
def get_patient(patient_id):
    current_user = get_current_user()
    if current_user.role == "patient" and current_user.patient_id != patient_id:
        return jsonify({"error": "Forbidden"}), 403

    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict())
