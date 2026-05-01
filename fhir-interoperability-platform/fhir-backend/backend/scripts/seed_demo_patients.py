from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.services.seed_service import seed_demo_patients
from app.db.database import db


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_demo_patients()
        db.session.commit()
        print("Demo patients seeded successfully.")
