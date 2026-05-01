from importlib import resources as impresources

import pandas as pd

from . import data


def get_bulk_data():
    inp_file = impresources.files(data) / 'Condition.ndjson'
    df = pd.read_json(inp_file, lines = True)
    return df 
