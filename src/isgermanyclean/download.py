from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError
import pandas as pd

from .utils import get_api_key, get_data, get_data_file

api_key = get_api_key()
client = EntsoePandasClient(api_key=api_key)


def download(opts):
    country = opts.country
    try:
        new_data = get_generation(country, opts.start, opts.end)
    except NoMatchingDataError:
        return
    if type(new_data.columns) == pd.MultiIndex:
        new_data = new_data.xs("Actual Aggregated", axis=1, level=1)
    try:
        data = get_data(country)
        update_from = new_data.index.min()
        data.update(new_data)
        new_index = new_data.index.difference(data.index)
        data = pd.concat([data, new_data.loc[new_index]])
    except FileNotFoundError:
        data = new_data
    data.dropna(inplace=True)
    data.sort_index(inplace=True)
    data.to_csv(get_data_file(country))


def get_generation(country, start, end):
    generation = client.query_generation(country, start=start, end=end, psr_type=None)
    hydro = ["Hydro Pumped Storage", "Hydro Run-of-river and poundage", "Hydro Water Reservoir"]
    for hc in hydro:
        sl = pd.IndexSlice[hc, :]
        if type(generation.columns) == pd.MultiIndex and hc in generation.columns:
            clipped = generation.loc[:, sl].fillna(value=0)
            generation.loc[:, sl] = clipped
    generation.dropna(inplace=True)
    generation = generation.resample("1H").mean()
    generation.index.name = "Timestamp"
    return generation
