from pandas.testing import assert_frame_equal
import pytest
import pandas as pd
import os

import sys

from src.ml_fhir.etl.observations import Observations

def test_imputation_glucose():
    """ Test that imputation works for glucose"""
    actual_df = pd.read_csv( os.path.join(os.path.dirname(__file__), '../data/q2-glucose-test.csv'))
    observations = Observations(os.path.join(os.path.dirname(__file__), '../data/test-observations.ndjson') , os.path.join(os.path.dirname(__file__), '../data/test-patients.ndjson') )
    glucose_df = observations.impute_observation(observations.data, observations.patient_df, "2339-0", 'glucose')

    assert_frame_equal(actual_df, glucose_df)

def test_imputation_triglycerides():
    """ Test that imputation works for triglycerides"""
    actual_df = pd.read_csv(  os.path.join(os.path.dirname(__file__), '../data/q2-tri-test.csv'))
    observations = Observations( os.path.join(os.path.dirname(__file__), '../data/test-observations.ndjson') ,  os.path.join(os.path.dirname(__file__), '../data/test-patients.ndjson'))
    triglycerides_df = observations.impute_observation(observations.data,observations.patient_df,"2571-8",'triglycerides')
    

    assert_frame_equal(actual_df, triglycerides_df)