from yahooquery import Ticker


def get_historical_data(ticker_list, start_date, end_date):
    tickers = Ticker(ticker_list)
    price_data_df = tickers.history(start=start_date, end=end_date)
    return price_data_df, tickers


# price_data_df.index.names
# price_data_df.describe()
# price_data_df.reset_index(inplace=True)
# price_data_df['date'][0]
# price_data_df["date"] = pd.to_datetime(price_data_df["date"])