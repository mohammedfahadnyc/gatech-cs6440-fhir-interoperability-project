def get_athena_data(patient):
    return {
        "name": patient.name,
        "patient_id": patient.id,
        "a1c": 8.1,
        "medications": ["Metformin", "Jardiance"],
        "diagnosis": "Type 2 Diabetes Mellitus",
        "note": "Imported from Athena system",
        "source_system": "Athena",
    }


def get_epic_data(patient):
    return {
        "name": patient.name,
        "patient_id": patient.id,
        "a1c": 7.4,
        "medications": ["Trulicity"],
        "diagnosis": "Type 2 Diabetes Mellitus",
        "note": "Imported from Epic system",
        "source_system": "Epic",
    }
