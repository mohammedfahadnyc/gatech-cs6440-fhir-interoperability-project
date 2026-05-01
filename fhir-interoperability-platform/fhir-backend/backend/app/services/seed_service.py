from datetime import date, timedelta

from app.db.database import db
from app.models.fhir_model import FHIRResource
from app.models.patient_model import Patient
from app.models.user_model import User
from app.services.fhir_converter import (
    build_condition,
    build_document_reference,
    build_medication_statement,
    build_observation,
    build_patient_resource,
)


DEMO_PATIENT_ROWS = [
    ("External Patient A", date(1988, 2, 14), "female", "external.demo1@example.local"),
    ("External Patient B", date(1979, 8, 9), "male", "external.demo2@example.local"),
    ("External Patient C", date(1991, 5, 21), "female", "external.demo3@example.local"),
    ("External Patient D", date(1984, 12, 3), "male", "external.demo4@example.local"),
]


def upsert_user(email, role, password, patient_id=None):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, role=role, patient_id=patient_id)
        db.session.add(user)
    else:
        user.role = role
        user.patient_id = patient_id

    user.set_password(password)
    return user


def add_resource(patient_id, resource_type, payload, source_system="seed"):
    db.session.add(
        FHIRResource(
            patient_id=patient_id,
            resource_type=resource_type,
            payload_json=payload,
            source_system=source_system,
        )
    )


def seed_demo_patients():
    for name, dob, gender, email in DEMO_PATIENT_ROWS:
        patient = Patient.query.filter_by(name=name).first()
        if not patient:
            patient = Patient(
                name=name,
                dob=dob,
                gender=gender,
                data_origin="external",
                is_authorized=False,
                is_imported=False,
                data_source=None,
            )
            db.session.add(patient)
            db.session.flush()
        upsert_user(email, "patient", "local-demo-password", patient.id)


def seed_data(reset=False):
    if reset:
        db.drop_all()

    db.create_all()

    clinician_emails = ["clinician.demo1@example.local", "clinician.demo2@example.local"]
    for email in clinician_emails:
        upsert_user(email, "clinician", "local-demo-password")

    patient_rows = [
        ("Internal Patient A", date(1978, 4, 12), "male", "patient.demo1@example.local"),
        ("Internal Patient B", date(1985, 7, 23), "female", "patient.demo2@example.local"),
        ("Internal Patient C", date(1969, 11, 2), "male", "patient.demo3@example.local"),
        ("Internal Patient D", date(1990, 1, 14), "female", "patient.demo4@example.local"),
        ("Internal Patient E", date(1975, 9, 30), "male", "patient.demo5@example.local"),
    ]
    hba1c_values = [5.7, 6.2, 7.1, 7.8, 8.4]
    medications = ["Metformin", "Jardiance", "Trulicity", "Prednisone"]
    baseline = date.today() - timedelta(days=365)

    for index, (name, dob, gender, email) in enumerate(patient_rows, start=1):
        patient = Patient(
            name=name,
            dob=dob,
            gender=gender,
            data_origin="internal",
            is_authorized=True,
            is_imported=True,
            data_source="internal",
        )
        db.session.add(patient)
        db.session.flush()

        upsert_user(email, "patient", "local-demo-password", patient.id)
        add_resource(patient.id, "Patient", build_patient_resource(patient), source_system="internal")
        add_resource(
            patient.id,
            "Condition",
            build_condition(
                patient.id,
                "Type 2 Diabetes Mellitus",
                baseline + timedelta(days=index * 7),
            ),
            source_system="internal",
        )

        for offset, value in enumerate(hba1c_values):
            observed_on = baseline + timedelta(days=offset * 90 + index * 3)
            add_resource(
                patient.id,
                "Observation",
                build_observation(patient.id, "HbA1c", value, observed_on),
                source_system="internal",
            )

        for med_index, medication in enumerate(medications):
            authored_on = baseline + timedelta(days=med_index * 60 + index * 5)
            add_resource(
                patient.id,
                "MedicationStatement",
                build_medication_statement(patient.id, medication, authored_on),
                source_system="internal",
            )

        add_resource(
            patient.id,
            "DocumentReference",
            build_document_reference(
                patient.id,
                f"{name} diabetes follow-up note. Encourage diet adherence and exercise.",
                "clinician.demo1@example.local",
            ),
            source_system="internal",
        )

    seed_demo_patients()
    db.session.commit()


def ensure_seed_data():
    db.create_all()

    if User.query.first():
        return False

    # Seed only empty databases so persisted Postgres data is preserved across restarts.
    seed_data(reset=False)
    return True
