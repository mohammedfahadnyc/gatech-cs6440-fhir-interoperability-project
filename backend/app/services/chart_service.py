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
