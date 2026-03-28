from flask import Blueprint, jsonify, request

from app.db.database import db
from app.middleware.rbac import get_current_user, role_required
from app.models.fhir_model import FHIRResource
from app.models.patient_model import Patient
from app.services.fhir_converter import convert_emr_payload
from app.services.mock_emr_service import get_athena_data, get_epic_data

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
    return jsonify([patient.to_summary_dict() for patient in patients])


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


@patient_bp.route("/<int:patient_id>/authorize", methods=["POST"])
@role_required("patient")
def authorize_patient(patient_id):
    """
    Authorize a patient for external data import from Athena or Epic.
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
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - source
          properties:
            source:
              type: string
              example: athena
    responses:
      200:
        description: Authorization stored
      400:
        description: Invalid source or internal patient
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    current_user = get_current_user()
    if current_user.patient_id != patient_id:
        return jsonify({"error": "Forbidden"}), 403

    payload = request.get_json(silent=True) or {}
    source = (payload.get("source") or "").strip().lower()
    if source not in {"athena", "epic"}:
        return jsonify({"error": "Source must be 'athena' or 'epic'"}), 400

    patient = Patient.query.get_or_404(patient_id)
    if patient.data_origin == "internal":
        return jsonify({"error": "Internal patients do not require authorization"}), 400

    patient.is_authorized = True
    patient.is_imported = False
    patient.data_source = source
    db.session.commit()

    return jsonify(patient.to_dict())


@patient_bp.route("/<int:patient_id>/import", methods=["POST"])
@role_required("clinician", "admin")
def import_patient_data(patient_id):
    """
    Import authorized patient data from the selected mock EMR source.
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
      201:
        description: Patient data imported
      400:
        description: Patient is not authorized or is internal
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    patient = Patient.query.get_or_404(patient_id)
    if patient.data_origin == "internal":
        return jsonify({"error": "Internal patients already have data"}), 400
    if not patient.is_authorized:
        return jsonify({"error": "Patient must be authorized before import"}), 400

    if patient.data_source == "athena":
        payload = get_athena_data(patient)
    elif patient.data_source == "epic":
        payload = get_epic_data(patient)
    else:
        return jsonify({"error": "Unsupported data source"}), 400

    FHIRResource.query.filter_by(patient_id=patient.id).delete()

    resources = convert_emr_payload(patient.id, payload)
    for resource_type, resource_payload in resources:
        db.session.add(
            FHIRResource(
                patient_id=patient.id,
                resource_type=resource_type,
                payload_json=resource_payload,
                source_system=payload["source_system"],
            )
        )

    patient.is_imported = True
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Patient data imported successfully",
                "patient": patient.to_dict(),
                "resource_count": len(resources),
            }
        ),
        201,
    )


@patient_bp.route("/<int:patient_id>/data", methods=["DELETE"])
@role_required("clinician", "admin")
def clear_patient_data(patient_id):
    """
    Clear patient clinical data and reset the demo state.
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
        description: Patient data cleared
      400:
        description: Internal patient data cannot be cleared here
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    patient = Patient.query.get_or_404(patient_id)
    if patient.data_origin == "internal":
        return jsonify({"error": "Internal patient data cannot be cleared with demo reset"}), 400

    FHIRResource.query.filter_by(patient_id=patient.id).delete()
    patient.is_authorized = False
    patient.is_imported = False
    patient.data_source = None
    db.session.commit()

    return jsonify({"message": "Patient data cleared", "patient": patient.to_dict()})
