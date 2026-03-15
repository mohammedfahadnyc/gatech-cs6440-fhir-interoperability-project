import base64
from datetime import date, datetime, timezone
from uuid import uuid4


def _iso_date(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def build_patient_resource(patient):
    return {
        "resourceType": "Patient",
        "id": f"patient-{patient.id}",
        "name": [{"text": patient.name}],
        "gender": patient.gender.lower(),
        "birthDate": patient.dob.isoformat(),
    }


def build_observation(patient_id, name, value, effective_date):
    return {
        "resourceType": "Observation",
        "id": str(uuid4()),
        "status": "final",
        "subject": {"reference": f"Patient/{patient_id}"},
        "code": {"text": name},
        "effectiveDateTime": _iso_date(effective_date),
        "valueQuantity": {"value": value, "unit": "%"},
    }


def build_medication_statement(patient_id, medication_name, authored_on=None):
    authored_on = authored_on or datetime.now(timezone.utc).date()
    return {
        "resourceType": "MedicationStatement",
        "id": str(uuid4()),
        "status": "active",
        "subject": {"reference": f"Patient/{patient_id}"},
        "medicationCodeableConcept": {"text": medication_name},
        "effectiveDateTime": _iso_date(authored_on),
    }


def build_condition(patient_id, condition_name, recorded_date=None):
    recorded_date = recorded_date or datetime.now(timezone.utc).date()
    return {
        "resourceType": "Condition",
        "id": str(uuid4()),
        "clinicalStatus": {"text": "active"},
        "subject": {"reference": f"Patient/{patient_id}"},
        "code": {"text": condition_name},
        "recordedDate": _iso_date(recorded_date),
    }


def build_document_reference(patient_id, note_text, author_email, created_at=None):
    created_at = created_at or datetime.now(timezone.utc)
    return {
        "resourceType": "DocumentReference",
        "id": str(uuid4()),
        "status": "current",
        "subject": {"reference": f"Patient/{patient_id}"},
        "date": created_at.isoformat(),
        "author": [{"display": author_email}],
        "description": "Clinical note",
        "content": [
            {
                "attachment": {
                    "contentType": "text/plain",
                    "data": base64.b64encode(note_text.encode("utf-8")).decode("utf-8"),
                }
            }
        ],
    }


def convert_emr_payload(patient_id, payload):
    resources = []
    observed_on = payload.get("observed_on") or datetime.now(timezone.utc).date()
    diagnosed_on = payload.get("diagnosed_on") or datetime.now(timezone.utc).date()

    if payload.get("a1c") is not None:
        resources.append(
            (
                "Observation",
                build_observation(patient_id, "HbA1c", payload["a1c"], observed_on),
            )
        )

    for medication in payload.get("medications", []):
        resources.append(
            (
                "MedicationStatement",
                build_medication_statement(patient_id, medication, observed_on),
            )
        )

    diagnosis = payload.get("diagnosis")
    if diagnosis:
        resources.append(
            ("Condition", build_condition(patient_id, diagnosis, diagnosed_on))
        )

    note_text = payload.get("note")
    if note_text:
        resources.append(
            (
                "DocumentReference",
                build_document_reference(
                    patient_id,
                    note_text,
                    payload.get("author_email", "system@import.local"),
                ),
            )
        )

    return resources
