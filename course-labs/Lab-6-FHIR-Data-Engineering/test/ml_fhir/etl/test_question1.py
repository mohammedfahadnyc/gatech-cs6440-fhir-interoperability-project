from pandas.testing import assert_frame_equal
import pytest
import pandas as pd
import os
import sys
from src.ml_fhir.etl.patients import Patients

import pytest

@pytest.fixture
def setup_patient():
    patients = Patients(os.path.join(os.path.dirname(__file__), '../data/test-patients.ndjson'))
    return patients

def test_age(setup_patient):
    """ Test that the get_age"""
    actual_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/q1-1-test.csv'))
    age_df = setup_patient.data
    age_df['age'] = age_df['birthDate'].apply(lambda x: setup_patient.get_age(x,'2023-11-05'))
    age_df = age_df[['id', 'age']]
    assert_frame_equal(actual_df, age_df)

def test_marital_status(setup_patient):
    """ Test that the get_marital_status """
    actual_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/q1-2-test.csv'))
    marital_df = setup_patient.data
    marital_df = setup_patient.get_marital_status(marital_df)
    marital_df = marital_df[['id','married_Divorced','married_Married','married_Widowed','married_Never Married' ]]
    assert_frame_equal(actual_df, marital_df)