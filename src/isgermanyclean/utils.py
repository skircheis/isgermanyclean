from json import load
from os import environ
from pandas import Timestamp
from pathlib import Path

today = Timestamp.today().floor("1D").tz_localize("Europe/Brussels")


def get_api_key():
    key_fname = "APIKEY"
    xdg_config_home = Path(environ["XDG_CONFIG_HOME"])
    key_file = xdg_config_home / "isgermanyclean" / key_fname
    with key_file.open() as f:
        return load(f)["api_key"]


def get_data_dir():
    try:
        xdg_data_home = Path(environ["XDG_DATA_HOME"])
    except KeyError:
        xdg_data_home = Path(environ["HOME"]) / ".local/share"
    return xdg_data_home / "isgermanyclean"


def get_data_file(country):
    return get_data_dir() / (country + ".csv")


def get_data(country, start=None, end=None):
    data_file = get_data_file(country)
    from pandas import read_csv

    data = read_csv(data_file, index_col="Timestamp", parse_dates=True)
    data = data.truncate(before=start, after=end)
    data.dropna(inplace=True)
    return data


def merge_data(datas):
    sufs = [" " + cc for cc in datas.keys()]
    vals = list(datas.values())
    merged = vals[0].merge(vals[1], how="inner", on="Timestamp", suffixes=sufs)
    return merged


def get_db():
    from sqlite3 import connect

    return connect(get_data_dir() / "database.db")
