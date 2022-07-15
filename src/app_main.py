# ASX Share Price Analysis
#

import json  # working with JSON formatted data
from pathlib import Path  # working with files/paths nicely
import streamlit as st

import altair as alt  # charting
import mplfinance as mpf
import pandas as pd  # 2-d arrays of data
import requests  # making http (web) requests
from pandas_cache import pd_cache, timeit
from yahooquery import Ticker

from helper_st_app import create_app_header
from load_asx_data import load_asx_company_data
from load_historical_data import get_historical_data

create_app_header("ASX 200 analyser")

start_date = st.sidebar.date_input("Start Date:")
end_date = st.sidebar.date_input("End Date:")

asx_code = st.sidebar.text_input("ASX code", value="CBA.AX")

#start_date.strftime('%m/%d/%Y')

# A list of companies in the [ASX 200](https://en.wikipedia.org/wiki/S%26P/ASX_200) index and
# their corresponding symbol (code/ticker); this includes their market cap (i.e. how much they are worth)
# which defines which companies are in the index. While this can and does change through time,
# changes to the composition of the index are typically slow.
# We also what market data and Yahoo Finance seems to provide this information for free

# #### ASX 200 - Index composition data
#
# This data set provided by the ASX is updated daily (or maybe the day following trading days).

# For example, the following function is designed to lookup the full company name from the ASX code.


def lookup_company_name_from_code(asx_code, asx_tickers_df):
    asx_code = asx_code.replace(".AX", "")
    try:
        return asx_tickers_df[asx_tickers_df["ASX code"] == asx_code][
            "Company name"].to_list()[0].title().replace(".", "")
    except Exception:
        return "Code not found"


# Here is another utility function that we are defining to get/extract the latest market cap information using
# the [API](https://www.mulesoft.com/resources/api/what-is-an-api) provided by the ASX.
# We are also returning the date associated with this information.
# Note that APIs often return information in particular formats.
# In this case the returned information is formatted as [JSON](https://www.json.org/json-en.html) and
# we have to parse it appropriately to get the precise details we are after.


def get_market_cap_from_code(asx_code):
    ASX_DATA_URL = "https://www.asx.com.au/asx/1/share/"
    asx_code = asx_code.replace(".AX", "")
    r = requests.get(ASX_DATA_URL + asx_code)
    data = json.loads(r.text)
    try:
        return data["market_cap"], data["last_trade_date"]
    except Exception:
        return None


# Cache the tickers file with the market cap information as it takes a few minutes to complete
# See `pd_cache` decorator. i.e. tmp directory `.pd_cache` directory.


@timeit
@pd_cache
def calculate_market_cap(asx_tickers_df):
    asx_tickers_df["market_cap"] = asx_tickers_df["ASX code"].apply(
        lambda _: get_market_cap_from_code(_)[0])
    return asx_tickers_df


def create_asx200_index():
    asx_tickers_df = load_asx_company_data()
    asx_tickers_df["companyname"] = asx_tickers_df["ticker"].apply(
        lambda _: lookup_company_name_from_code(_))
    asx_tickers_df = calculate_market_cap(asx_tickers_df)
    return asx_tickers_df.sort_values(by='market_cap',
                                      ascending=False).reset_index()[:200]


# See also: https://asxportfolio.com/shares-python-for-finance-getting-stock-data
# Example ASX API to get latest data -  e.g. CBA: https://www.asx.com.au/asx/1/share/CBA

# * Allow user to choose from this list in a sensible manner e.g. lookup and/or predefined favourites list.
# * Display the price history and other relevant information for each company selected in an appealing manner
# (to aide comparison of their relative performance). e.g. may want to look over past year, 6m, 3m, 1m, 1w etc.

asx_tickers_df = load_asx_company_data()

price_data_df, tickers = get_historical_data([asx_code], start_date, end_date)

price_data_df

# tickers.key_stats
# tickers.summary_detail
profile = tickers.asset_profile
profile[asx_code]['website']

price_data_df["symbol"] = price_data_df.index.get_level_values(0)
price_data_df["date"] = pd.to_datetime(price_data_df.index.get_level_values(1))

price_data_df

def create_close_price_chart(asx_code, price_data_df):
    chart_data_df = price_data_df[price_data_df["symbol"] == asx_code]
    c = alt.Chart(chart_data_df).mark_circle().encode(x='date', y='adjclose')
    chart_data_df.set_index('date', inplace=True)
    mpf.plot(chart_data_df,
             type='line',
             volume=True,
             show_nontrading=True,
             datetime_format='%d-%b-%Y')
    mpf.show(c)


# create_close_price_chart(asx_code, price_data_df) <-- not currently working