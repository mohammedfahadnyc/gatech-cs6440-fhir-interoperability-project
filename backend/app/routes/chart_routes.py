from flask import Blueprint, jsonify, request

from app.db.database import db
from app.middleware.rbac import get_current_user, patient_scope_required, role_required
from app.models.fhir_model import FHIRResource
from app.models.patient_model import Patient
from app.services.chart_service import (
    get_patient_chart,
    get_patient_fhir_bundle,
    get_patient_summary,
)
from app.services.fhir_converter import build_document_reference

chart_bp = Blueprint("charts", __name__)


@chart_bp.route("/<int:patient_id>/chart", methods=["GET"])
@role_required("clinician", "admin", "patient")
def patient_chart(patient_id):
    """
    Get the UI-friendly patient chart payload.
    ---
    tags:
      - Chart
    security:
      - Bearer: []
    parameters:
      - in: path
        name: patient_id
        required: true
        type: integer
    responses:
      200:
        description: Patient chart
      401:
        description: Missing or invalid token
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    scope_error = patient_scope_required(patient_id)
    if scope_error:
        return scope_error
    return jsonify(get_patient_chart(patient_id))


@chart_bp.route("/<int:patient_id>/summary", methods=["GET"])
@role_required("clinician", "admin", "patient")
def patient_summary(patient_id):
    """
    Get lightweight dashboard summary stats for a patient.
    ---
    tags:
      - Chart
    security:
      - Bearer: []
    parameters:
      - in: path
        name: patient_id
        required: true
        type: integer
    responses:
      200:
        description: Patient summary
      401:
        description: Missing or invalid token
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    scope_error = patient_scope_required(patient_id)
    if scope_error:
        return scope_error
    return jsonify(get_patient_summary(patient_id))


@chart_bp.route("/<int:patient_id>/fhir", methods=["GET"])
@role_required("clinician", "admin", "patient")
def patient_fhir_bundle(patient_id):
    """
    Export all stored FHIR resources for a patient as a FHIR Bundle.
    ---
    tags:
      - FHIR
    security:
      - Bearer: []
    parameters:
      - in: path
        name: patient_id
        required: true
        type: integer
    responses:
      200:
        description: FHIR Bundle export
      401:
        description: Missing or invalid token
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    scope_error = patient_scope_required(patient_id)
    if scope_error:
        return scope_error
    return jsonify(get_patient_fhir_bundle(patient_id))


@chart_bp.route("/<int:patient_id>/notes", methods=["POST"])
@role_required("clinician", "admin")
def create_note(patient_id):
    """
    Create a clinical note stored as a FHIR DocumentReference.
    ---
    tags:
      - Notes
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
            - note
          properties:
            note:
              type: string
              example: Patient reports improved glucose control over the last month.
    responses:
      201:
        description: Note created
      400:
        description: Missing note text
      401:
        description: Missing or invalid token
      403:
        description: Forbidden
      404:
        description: Patient not found
    """
    Patient.query.get_or_404(patient_id)

    payload = request.get_json(silent=True) or {}
    note_text = (payload.get("note") or "").strip()
    if not note_text:
        return jsonify({"error": "Note text is required"}), 400

    current_user = get_current_user()
    resource_payload = build_document_reference(patient_id, note_text, current_user.email)
    resource = FHIRResource(
        patient_id=patient_id,
        resource_type="DocumentReference",
        payload_json=resource_payload,
        source_system="manual_note",
    )
    db.session.add(resource)
    db.session.commit()

    return jsonify(resource.to_dict()), 201
