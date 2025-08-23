from sqlalchemy import create_engine
import pandas as pd

def get_db_engine(user, password, host, port, db):
    """
    Creates and returns a SQLAlchemy engine for a MySQL database.

    Args:
        user (str): Database username.
        password (str): Database password.
        host (str): Database host.
        port (int): Database port.
        db (str): Database name.

    Returns:
        sqlalchemy.engine.Engine: The database engine, or None on failure.
    """
    try:
        # Format for mysql+pymysql: mysql+pymysql://<user>:<password>@<host>[:<port>]/<dbname>
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
        engine = create_engine(connection_string, echo=False)
        print("Database engine created successfully.")
        return engine
    except Exception as e:
        print(f"Failed to create database engine: {e}")
        return None

def save_df_to_db(df: pd.DataFrame, table_name: str, engine, if_exists='append'):
    """
    Saves a pandas DataFrame to a table in the database.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        table_name (str): The name of the table.
        engine (sqlalchemy.engine.Engine): The database engine.
        if_exists (str): How to behave if the table exists ('fail', 'replace', or 'append').
                         Defaults to 'append'.
    """
    if df is None or df.empty:
        print("DataFrame is empty. Nothing to save to the database.")
        return

    try:
        print(f"Attempting to save {len(df)} rows to table '{table_name}'...")
        # Use pandas to_sql to write to the database.
        # This will create the table on the first run and append data on subsequent runs.
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        print(f"Successfully saved data to table '{table_name}'.")
    except Exception as e:
        print(f"An error occurred while saving data to the database: {e}")
