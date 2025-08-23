import tushare as ts
import pandas as pd

def fetch_15min_data(token: str, ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches 15-minute frequency stock data from Tushare.

    Args:
        token (str): Your Tushare API token.
        ts_code (str): The stock code, e.g., '000001.SZ'.
        start_date (str): The start date, e.g., '2023-01-01'.
        end_date (str): The end date, e.g., '2023-01-31'.

    Returns:
        pd.DataFrame: A pandas DataFrame with the 15-minute data, or None if an error occurs.
    """
    try:
        pro = ts.pro_api(token)

        # Tushare's stk_mins expects 'YYYY-MM-DD HH:MM:SS' format.
        # We'll cover the full day from market open to close.
        start_datetime = f"{start_date} 09:00:00"
        end_datetime = f"{end_date} 16:00:00"

        print(f"Fetching 15min data for {ts_code} from {start_datetime} to {end_datetime}...")

        df = pro.stk_mins(ts_code=ts_code, start_date=start_datetime, end_date=end_datetime, freq='15min')

        if df is not None and not df.empty:
            print(f"Successfully fetched {len(df)} records for {ts_code}.")
        else:
            print(f"No data returned for {ts_code} for the specified period.")

        return df
    except Exception as e:
        print(f"An error occurred while fetching data for {ts_code}: {e}")
        return None
