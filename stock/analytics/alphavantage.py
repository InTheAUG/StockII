# TODO: Build statistics method for Stock
# TODO: getetf; getindexes;
import time
from warnings import warn

from stock.analytics.tech_analysis import buildtechanalysis
from stock.paths import STOCKFILES, PACKAGE_BASEPATH, SETTINGS_PATH
from stock.analytics.error import InvalidServerResponseError
from pathlib import Path

import os
import toml
import pandas as pd
import requests

SETTINGS = toml.load(Path(__file__) / "settings.toml")
ALPHAVANTAGE_KEY_VAR = SETTINGS["alphavantage"]["api_key_var"]

# =======================HELPER FUNCTIONS=======================#
def save_response(response, file, filetype, save_log=False):
    if save_log:
        with open(STOCKFILES + file + ".log", "a") as f:
            f.write(response.content.decode("utf-8"))

    with open(STOCKFILES + "sector." + filetype, "w") as f:
        f.write(response.text)


def checkValidResponse(response):
    if response.status_code != 200:
        raise InvalidServerResponseError(
            f"[-]Invalid server response with Code: {response.status_code} @Sector"
        )

    if "Invalid API call" in response.text or response.text == "{}":
        return False

    return True


def reverse_df(df):
    return df[::-1]


# =======================Data Acquisition=======================#
def getsector(save_log=False):
    data = {
        "function": "sector",
        "apikey": os.getenv(ALPHAVANTAGE_KEY_VAR, default="Hamakavula"),
    }

    response = requests.get("https://www.alphavantage.co/query", params=data, timeout=8)

    if not checkValidResponse(response):
        warn("[-]Could not fetch sector data from Alphavantage.", stacklevel=1)

    response.encoding = "utf-8"

    save_response(response, "sector", ".json", save_log=save_log)

    return


def getstock(
    symbol,
    size="compact",
    interval="15min",
    mode="TIME_SERIES_DAILY_ADJUSTED",
    save_log=False,
):

    key = os.getenv(ALPHAVANTAGE_KEY_VAR, False)

    if not key:
        raise EnvironmentError("Environment was not initialized.")

    data = {
        "function": mode,
        "symbol": symbol,
        "outputsize": size,
        "datatype": "csv",
        "apikey": key,
    }

    if mode == "TIME_SERIES_INTRADAY":
        data["interval"] = interval

    response = requests.get("https://www.alphavantage.co/query", params=data, timeout=8)

    response.encoding = "utf-8"

    if not checkValidResponse(response):
        warn("[-]Response to stock request for {} failed.".format(symbol), stacklevel=2)
        return
    save_response(response, symbol, "csv", save_log=save_log)

    return


def getstocklist(
    namelist,
    size="compact",
    interval="15min",
    mode="TIME_SERIES_DAILY_ADJUSTED",
    save_log=False,
    freq=12,
):

    for name in namelist:
        getstock(name, size=size, interval=interval, mode=mode, save_log=save_log)
        time.sleep(freq)


def append_col_names(df, exclude, append_val):

    col_list = list(df.columns)

    if isinstance(exclude, list):
        for val in exclude:
            col_list.remove(val)
    else:
        col_list.remove(exclude)

    val_dict = dict(zip(col_list, [x + "_{}".format(append_val) for x in col_list]))

    df.rename(columns=val_dict, inplace=True)

    return df


def build_df():

    files = os.listdir(STOCKFILES)

    if not files:
        return None

    stocks = [x for x in files if ".csv" in x]

    df = reverse_df(pd.read_csv(STOCKFILES + stocks[0]))
    df = append_col_names(buildtechanalysis(df), "timestamp", stocks[0].split(".")[0])

    for stock in stocks[1:]:
        current = append_col_names(
            buildtechanalysis(reverse_df(pd.read_csv(STOCKFILES + stock))),
            "timestamp",
            stock.split(".")[0],
        )
        df = df.merge(current, sort=True, how="outer", on="timestamp")

    df.set_index("timestamp", inplace=True)
    df.interpolate(method="time", inplace=True)

    return df
