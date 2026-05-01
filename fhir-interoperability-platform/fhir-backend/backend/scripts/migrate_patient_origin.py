from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.services.patient_compat_service import (
    ensure_patient_demo_columns,
    migrate_existing_patients_to_internal,
)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        ensure_patient_demo_columns()
        migrate_existing_patients_to_internal()
        print("Patient origin migration completed.")
