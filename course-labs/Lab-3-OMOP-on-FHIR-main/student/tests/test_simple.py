
import datetime
from decimal import Decimal
from student_code import get_measurement_value, get_patient_name, get_patient_gender_as_string

def test_get_measurement_value():
    row = (2, 1, 3013290, datetime.date(2013, 4, 2), datetime.datetime(2013, 4, 2, 9, 30, 10), None, 0, None, Decimal('6.2'), None, 44777602, Decimal('4.8'), Decimal('6.0'), None, None, None, None, 3013290, 'kPa', None, '6.2', None, None)
    student_answer = get_measurement_value(row)
    correct_answer = 6.2
    assert student_answer == correct_answer

def test_get_patient_name():
    row = (1, 'Keeling', 'Abdul', None, 'Mr.', None, None, None, 0, 'phone:home:555-539-7338', None, None, 'M')
    student_answer = get_patient_name(row)
    correct_answer = "Abdul Keeling"
    assert student_answer == correct_answer

def test_get_patient_gender_as_string():
    row = (2, 8532, 2128, None, None, None, 8527, 0, None, None, None, '10002723', 'F', 0, 'WHITE', 2000001404, None, 0, 8532, 'FEMALE', 'Gender', 'Gender', 'Gender', 'S', 'F', datetime.date(1970, 1, 1), datetime.date(2099, 12, 31), None)
    keys = ['person_id', 'gender_concept_id', 'year_of_birth', 'month_of_birth', 'day_of_birth', 'birth_datetime', 'race_concept_id', 'ethnicity_concept_id', 'location_id', 'provider_id', 'care_site_id', 'person_source_value', 'gender_source_value', 'gender_source_concept_id', 'race_source_value', 'race_source_concept_id', 'ethnicity_source_value', 'ethnicity_source_concept_id', 'concept_id', 'concept_name', 'domain_id', 'vocabulary_id', 'concept_class_id', 'standard_concept', 'concept_code', 'valid_start_date', 'valid_end_date', 'invalid_reason']
    student_answer = get_patient_gender_as_string(row, keys)
    correct_answer = "FEMALE"
    assert student_answer == correct_answer