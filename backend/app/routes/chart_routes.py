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
    scope_error = patient_scope_required(patient_id)
    if scope_error:
        return scope_error
    return jsonify(get_patient_chart(patient_id))


@chart_bp.route("/<int:patient_id>/summary", methods=["GET"])
@role_required("clinician", "admin", "patient")
def patient_summary(patient_id):
    scope_error = patient_scope_required(patient_id)
    if scope_error:
        return scope_error
    return jsonify(get_patient_summary(patient_id))


@chart_bp.route("/<int:patient_id>/fhir", methods=["GET"])
@role_required("clinician", "admin", "patient")
def patient_fhir_bundle(patient_id):
    scope_error = patient_scope_required(patient_id)
    if scope_error:
        return scope_error
    return jsonify(get_patient_fhir_bundle(patient_id))


@chart_bp.route("/<int:patient_id>/notes", methods=["POST"])
@role_required("clinician", "admin")
def create_note(patient_id):
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
