import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Configuration class for the Flask application, loading settings from environment variables
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-for-fhir-bridge-2026")
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "dev-jwt-secret-key-for-fhir-bridge-2026"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://fhir:fhir@localhost:5432/fhir_bridge"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    AUTO_SEED = os.getenv("AUTO_SEED", "false").lower() == "true"
    EPIC_ENABLED = os.getenv("EPIC_ENABLED", "false").lower() == "true"
    EPIC_CLIENT_ID = os.getenv("EPIC_CLIENT_ID", "")
    EPIC_CLIENT_SECRET = os.getenv("EPIC_CLIENT_SECRET", "")
    EPIC_REDIRECT_URI = os.getenv(
        "EPIC_REDIRECT_URI", "http://127.0.0.1:5000/auth/epic/callback"
    )
    EPIC_FHIR_BASE_URL = os.getenv(
        "EPIC_FHIR_BASE_URL",
        "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4",
    )
    EPIC_AUTH_BASE_URL = os.getenv(
        "EPIC_AUTH_BASE_URL", "https://fhir.epic.com/interconnect-fhir-oauth/"
    )
    EPIC_DEMO_PATIENT_EMAILS = os.getenv(
        "EPIC_DEMO_PATIENT_EMAILS",
        "nina.patel@patient.com,chris.walker@patient.com",
    )
    FRONTEND_APP_URL = os.getenv("FRONTEND_APP_URL", "")
