import pandas as pd
from sqlalchemy import create_engine, text

def push_to_database():
    # Database connection string (Update password as needed)
    db_uri = "mysql+pymysql://root:password@localhost:3306/Enterprise_Recon_DB"
    engine = create_engine(db_uri)

    files = [
        {"file": "data/era_summary_load.csv", "table": "tbl_era_summary"},
        {"file": "data/era_claims_load.csv", "table": "tbl_era_claims"},
        {"file": "data/bank_feed_load.csv", "table": "tbl_bank_feed"}
    ]

    for item in files:
        print(f"Reading {item['file']}...")
        try:
            df = pd.read_csv(item['file'])
            
            # Format dates for SQL if importing summary
            if item['table'] == 'tbl_era_summary':
                df['Check_Date'] = pd.to_datetime(df['Check_Date'], format='%m/%d/%y').dt.strftime('%Y-%m-%d')
                
        except FileNotFoundError:
            print(f"Error: Could not find {item['file']}. Skipping.")
            continue

        try:
            with engine.begin() as conn:
                print(f"Clearing old data from {item['table']}...")
                # Temporarily disable foreign key checks to truncate
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
                conn.execute(text(f"TRUNCATE TABLE {item['table']};"))
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
                
            print(f"Pushing new data to {item['table']}...")
            df.to_sql(name=item['table'], con=engine, if_exists='append', index=False)
            
            print(f"Success! Loaded {len(df)} records into {item['table']}.\n")
            
        except Exception as e:
            print(f"An error occurred during database import for {item['table']}: {e}\n")

if __name__ == "__main__":
    push_to_database()import pandas as pd
from sqlalchemy import create_engine, text

def push_to_database():
    # Database connection string (Update password as needed)
    db_uri = "mysql+pymysql://root:password@localhost:3306/Enterprise_Recon_DB"
    engine = create_engine(db_uri)

    files = [
        {"file": "data/era_summary_load.csv", "table": "tbl_era_summary"},
        {"file": "data/era_claims_load.csv", "table": "tbl_era_claims"},
        {"file": "data/bank_feed_load.csv", "table": "tbl_bank_feed"}
    ]

    for item in files:
        print(f"Reading {item['file']}...")
        try:
            df = pd.read_csv(item['file'])
            
            # Format dates for SQL if importing summary
            if item['table'] == 'tbl_era_summary':
                df['Check_Date'] = pd.to_datetime(df['Check_Date'], format='%m/%d/%y').dt.strftime('%Y-%m-%d')
                
        except FileNotFoundError:
            print(f"Error: Could not find {item['file']}. Skipping.")
            continue

        try:
            with engine.begin() as conn:
                print(f"Clearing old data from {item['table']}...")
                # Temporarily disable foreign key checks to truncate
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
                conn.execute(text(f"TRUNCATE TABLE {item['table']};"))
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
                
            print(f"Pushing new data to {item['table']}...")
            df.to_sql(name=item['table'], con=engine, if_exists='append', index=False)
            
            print(f"Success! Loaded {len(df)} records into {item['table']}.\n")
            
        except Exception as e:
            print(f"An error occurred during database import for {item['table']}: {e}\n")

if __name__ == "__main__":
    push_to_database()