import pandas as pd

from bulk_fhir.dataloader import get_bulk_data

def test_get_bulk_data():
    df = get_bulk_data()
    assert type(df) == pd.DataFrame
