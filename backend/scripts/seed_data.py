from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.services.seed_service import seed_data


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_data(reset=True)
        print("Seed data created successfully.")
