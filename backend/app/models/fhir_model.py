from datetime import datetime, timezone

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB

from app.db.database import db

json_type = JSON().with_variant(JSONB, "postgresql")


class FHIRResource(db.Model):
    __tablename__ = "fhir_resources"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    resource_type = db.Column(db.String(80), nullable=False, index=True)
    payload_json = db.Column(json_type, nullable=False)
    source_system = db.Column(db.String(100), nullable=False, default="unknown")
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    patient = db.relationship("Patient", back_populates="fhir_resources")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "resource_type": self.resource_type,
            "payload_json": self.payload_json,
            "source_system": self.source_system,
            "created_at": self.created_at.isoformat(),
        }
