import configparser
import argparse
from datetime import datetime, timedelta

# Import our custom modules
import data_fetcher
import database

def main():
    """
    Main function to run the data fetching and storing process.
    """
    # --- 1. Read Configuration ---
    config = configparser.ConfigParser()
    try:
        # Note: The script is run from the root of the project,
        # so the path to config.ini is relative to that.
        config.read('tushare_project/config.ini')

        # Tushare config
        tushare_token = config['tushare']['token']

        # MySQL config
        mysql_host = config['mysql']['host']
        mysql_user = config['mysql']['user']
        mysql_pass = config['mysql']['password']
        mysql_db = config['mysql']['database']
        mysql_port = int(config['mysql']['port'])
        table_name = config['mysql']['table_name']

    except KeyError as e:
        print(f"Error: Missing configuration key {e} in config.ini.")
        print("Please make sure your config.ini is correctly formatted.")
        return
    except Exception as e:
        print(f"Error reading config.ini: {e}")
        return

    if 'YOUR_TUSHARE_TOKEN' in tushare_token:
        print("Error: Please replace 'YOUR_TUSHARE_TOKEN' with your actual Tushare token in config.ini")
        return

    # --- 2. Parse Command-line Arguments ---
    parser = argparse.ArgumentParser(description="Fetch Tushare 15-minute stock data and save to MySQL.")

    parser.add_argument('--code', type=str, required=True, help="The stock code (ts_code), e.g., '000001.SZ'.")

    # Default to yesterday
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    parser.add_argument('--start', type=str, default=yesterday, help="Start date in YYYY-MM-DD format. Defaults to yesterday.")
    parser.add_argument('--end', type=str, default=yesterday, help="End date in YYYY-MM-DD format. Defaults to yesterday.")

    args = parser.parse_args()

    ts_code = args.code
    start_date = args.start
    end_date = args.end

    print(f"--- Starting Process for {ts_code} ---")
    print(f"Date Range: {start_date} to {end_date}")

    # --- 3. Fetch Data from Tushare ---
    stock_data = data_fetcher.fetch_15min_data(tushare_token, ts_code, start_date, end_date)

    if stock_data is None or stock_data.empty:
        print("No data was fetched. Exiting.")
        return

    # --- 4. Connect to Database and Save Data ---
    db_engine = database.get_db_engine(
        user=mysql_user,
        password=mysql_pass,
        host=mysql_host,
        port=mysql_port,
        db=mysql_db
    )

    if db_engine is None:
        print("Could not connect to the database. Exiting.")
        return

    database.save_df_to_db(stock_data, table_name, db_engine)

    print(f"--- Process for {ts_code} finished successfully! ---")


if __name__ == '__main__':
    main()
