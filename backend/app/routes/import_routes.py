from datetime import datetime

from flask import Blueprint, jsonify, request

from app.db.database import db
from app.middleware.rbac import role_required
from app.models.fhir_model import FHIRResource
from app.models.patient_model import Patient
from app.services.fhir_converter import build_patient_resource, convert_emr_payload

import_bp = Blueprint("imports", __name__)


def _parse_date(value, fallback):
    if not value:
        return fallback
    return datetime.fromisoformat(value).date()


@import_bp.route("/import", methods=["POST"])
@role_required("clinician", "admin")
def import_emr_payload():
    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Patient name is required"}), 400

    patient_id = payload.get("patient_id")
    patient = Patient.query.get(patient_id) if patient_id else None

    if not patient:
        dob = _parse_date(payload.get("dob"), datetime(1980, 1, 1).date())
        gender = (payload.get("gender") or "unknown").lower()
        patient = Patient(name=name, dob=dob, gender=gender)
        db.session.add(patient)
        db.session.flush()

        # Every patient gets a canonical FHIR Patient resource in the clinical store.
        db.session.add(
            FHIRResource(
                patient_id=patient.id,
                resource_type="Patient",
                payload_json=build_patient_resource(patient),
                source_system=payload.get("source_system", "emr_import"),
            )
        )

    resources = convert_emr_payload(patient.id, payload)
    # Converted FHIR resources are persisted as-is so downstream consumers can stay FHIR-first.
    for resource_type, resource_payload in resources:
        db.session.add(
            FHIRResource(
                patient_id=patient.id,
                resource_type=resource_type,
                payload_json=resource_payload,
                source_system=payload.get("source_system", "emr_import"),
            )
        )

    db.session.commit()

    return (
        jsonify(
            {
                "message": "EMR payload imported successfully",
                "patient": patient.to_dict(),
                "resource_count": len(resources) + (0 if patient_id else 1),
            }
        ),
        201,
    )
