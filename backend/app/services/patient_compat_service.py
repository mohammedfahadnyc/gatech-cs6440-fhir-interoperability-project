from sqlalchemy import text

from app.db.database import db


def ensure_patient_demo_columns():
    statements = [
        "ALTER TABLE patients ADD COLUMN IF NOT EXISTS is_authorized BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE patients ADD COLUMN IF NOT EXISTS is_imported BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE patients ADD COLUMN IF NOT EXISTS data_source VARCHAR(100)",
        "ALTER TABLE patients ADD COLUMN IF NOT EXISTS data_origin VARCHAR(50) NOT NULL DEFAULT 'internal'",
    ]

    for statement in statements:
        db.session.execute(text(statement))
    db.session.commit()


def migrate_existing_patients_to_internal():
    db.session.execute(
        text(
            """
            UPDATE patients
            SET data_origin = 'internal',
                is_authorized = TRUE,
                is_imported = TRUE,
                data_source = 'internal'
            WHERE data_origin IS NULL
               OR data_origin = ''
               OR data_origin = 'internal'
            """
        )
    )
    db.session.commit()
