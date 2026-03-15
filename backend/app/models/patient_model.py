from datetime import datetime, timezone

from app.db.database import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    users = db.relationship("User", back_populates="patient", lazy=True)
    fhir_resources = db.relationship(
        "FHIRResource",
        back_populates="patient",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dob": self.dob.isoformat(),
            "gender": self.gender,
            "created_at": self.created_at.isoformat(),
        }
