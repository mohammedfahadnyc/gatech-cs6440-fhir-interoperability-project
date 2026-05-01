from pandas.testing import assert_frame_equal
import pytest
import pandas as pd
import os 
import sys

from src.ml_fhir.etl.observations import Observations

def test_mean_norm_glucose():
    """ Test mean normilization works"""
    test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/q2-glucose-test.csv'))
    actual_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/q3-test.csv'))
    observations = Observations(os.path.join(os.path.dirname(__file__), '../data/test-observations.ndjson') , os.path.join(os.path.dirname(__file__), '../data/test-patients.ndjson') )
    test_df['glucose'] = observations.mean_normalize(test_df, 'glucose')

    assert_frame_equal(actual_df, test_df)
