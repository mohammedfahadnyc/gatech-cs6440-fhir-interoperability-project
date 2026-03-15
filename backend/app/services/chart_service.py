from app.models.fhir_model import FHIRResource
from app.models.patient_model import Patient


def get_patient_chart(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    resources = FHIRResource.query.filter_by(patient_id=patient_id).all()

    # The chart payload is intentionally frontend-shaped to keep dashboard code simple.
    chart = {
        "patient": patient.to_dict(),
        "observations": [],
        "medications": [],
        "conditions": [],
        "notes": [],
    }

    for resource in resources:
        payload = resource.payload_json
        if resource.resource_type == "Observation":
            chart["observations"].append(payload)
        elif resource.resource_type == "MedicationStatement":
            chart["medications"].append(payload)
        elif resource.resource_type == "Condition":
            chart["conditions"].append(payload)
        elif resource.resource_type == "DocumentReference":
            chart["notes"].append(payload)

    chart["observations"].sort(key=lambda item: item.get("effectiveDateTime", ""))
    chart["medications"].sort(key=lambda item: item.get("effectiveDateTime", ""))
    chart["conditions"].sort(key=lambda item: item.get("recordedDate", ""))
    chart["notes"].sort(key=lambda item: item.get("date", ""))

    return chart


def get_patient_summary(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    resources = FHIRResource.query.filter_by(patient_id=patient.id).all()

    latest_a1c = None
    latest_a1c_date = ""
    medication_names = set()
    note_count = 0
    last_visit = ""

    for resource in resources:
        payload = resource.payload_json
        if resource.resource_type == "Observation":
            effective_date = payload.get("effectiveDateTime", "")
            value_quantity = payload.get("valueQuantity") or {}
            if payload.get("code", {}).get("text") == "HbA1c" and effective_date >= latest_a1c_date:
                latest_a1c_date = effective_date
                latest_a1c = value_quantity.get("value")
            if effective_date > last_visit:
                last_visit = effective_date
        elif resource.resource_type == "MedicationStatement":
            medication = payload.get("medicationCodeableConcept", {}).get("text")
            if medication:
                medication_names.add(medication)
            effective_date = payload.get("effectiveDateTime", "")
            if effective_date > last_visit:
                last_visit = effective_date
        elif resource.resource_type == "DocumentReference":
            note_count += 1
            note_date = payload.get("date", "")
            visit_date = note_date[:10] if note_date else ""
            if visit_date > last_visit:
                last_visit = visit_date

    return {
        "patient_id": patient.id,
        "latest_a1c": latest_a1c,
        "medication_count": len(medication_names),
        "note_count": note_count,
        "last_visit": last_visit or None,
    }


def get_patient_fhir_bundle(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    resources = FHIRResource.query.filter_by(patient_id=patient.id).order_by(FHIRResource.created_at.asc()).all()

    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": resource.payload_json} for resource in resources],
    }
