import pytest

from bulk_fhir.dataloader import get_bulk_data
from bulk_fhir.eda import count_all_prediabetes, count_prediabetes_timerange, predict_future_cumulative_prediabetes, fhir_bulk_exporter_top3_procedures


@pytest.fixture
def sample_dataframe():
    return get_bulk_data()


def test_count_all_prediabetes(sample_dataframe):
    res = count_all_prediabetes(sample_dataframe)
    assert isinstance(res, int)
    assert res > 0


def test_count_all_prediabetes_timerange(sample_dataframe):
    res = count_prediabetes_timerange(sample_dataframe, 1950, 1970)
    assert isinstance(res, int)
    assert res == 0


def test_predict_future_cumulative_prediabetes(sample_dataframe):
    res = predict_future_cumulative_prediabetes(sample_dataframe, 2024)
    assert isinstance(res, float)
    assert res > 0


def test_fhir_bulk_exporter_top3_procedures():
    res = fhir_bulk_exporter_top3_procedures()
    assert len(res) == 3
