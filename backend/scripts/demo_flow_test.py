from pathlib import Path
import json
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.models.patient_model import Patient


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        patient = Patient.query.filter_by(data_origin="external").order_by(Patient.id.asc()).first()
        if not patient:
            raise SystemExit("No external demo patient found. Run backend/scripts/seed_demo_patients.py first.")
        patient_id = patient.id

    client = app.test_client()
    login = client.post(
        "/auth/login",
        json={"email": "doctor1@clinic.com", "password": "password123"},
    )
    token = login.get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    authorize_response = client.post(
        f"/patients/{patient_id}/authorize",
        headers=headers,
        json={"source": "athena"},
    )
    print("Authorize:", authorize_response.status_code, authorize_response.get_json())

    import_response = client.post(f"/patients/{patient_id}/import", headers=headers)
    print("Import:", import_response.status_code, import_response.get_json())

    chart_response = client.get(f"/patients/{patient_id}/chart", headers=headers)
    print("Chart:")
    print(json.dumps(chart_response.get_json(), indent=2))
