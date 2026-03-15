from flask import Blueprint, jsonify

from app.middleware.rbac import get_current_user, role_required
from app.models.patient_model import Patient

patient_bp = Blueprint("patients", __name__)


@patient_bp.route("", methods=["GET"])
@role_required("clinician", "admin")
def list_patients():
    """
    List all patients.
    ---
    tags:
      - Patients
    security:
      - Bearer: []
    responses:
      200:
        description: Patient list
      401:
        description: Missing or invalid token
      403:
        description: Forbidden
    """
    patients = Patient.query.order_by(Patient.name.asc()).all()
    return jsonify([patient.to_dict() for patient in patients])


@patient_bp.route("/<int:patient_id>", methods=["GET"])
@role_required("clinician", "admin", "patient")
def get_patient(patient_id):
    """
    Get one patient.
    ---
    tags:
      - Patients
    security:
      - Bearer: []
    parameters:
      - in: path
        name: patient_id
        required: true
        type: integer
    responses:
      200:
        description: Patient record
      401:
        description: Missing or invalid token
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    current_user = get_current_user()
    if current_user.role == "patient" and current_user.patient_id != patient_id:
        return jsonify({"error": "Forbidden"}), 403

    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict())
