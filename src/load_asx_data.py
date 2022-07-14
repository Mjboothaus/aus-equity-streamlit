import pandas as pd

def load_asx_company_data():
    ASX_TICKERS_URL = "https://www.asx.com.au/asx/research/ASXListedCompanies.csv"
    try:
        return pd.read_csv(ASX_TICKERS_URL, skiprows=1)
    except Exception:
        return None
