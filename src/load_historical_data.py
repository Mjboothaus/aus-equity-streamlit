
from yahooquery import Ticker


def get_historical_data(ticker_list, start_date, end_date):
    tickers = Ticker(ticker_list)
    price_data_df = tickers.history(start=start_date, end=end_date)
    return price_data_df, tickers

# ticker_list = "CBA.AX WBC.AX IAG.AX"
# start_date = "2021-01-01"
# end_date = "2021-12-31"

price_data_df, tickers = get_historical_data()

tickers.key_stats;
tickers.summary_detail;

profile = tickers.asset_profile


# profile['CBA.AX']['website']
# profile['WBC.AX']['website']


price_data_df.index.names
price_data_df.describe()
price_data_df.reset_index(inplace=True)
price_data_df['date'][0]
price_data_df["date"] = pd.to_datetime(price_data_df["date"])