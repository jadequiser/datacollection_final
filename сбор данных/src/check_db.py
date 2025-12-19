import sqlite3
import pandas as pd
import os

def check_data():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'app.db')
    
    print(f"Searching for database in {db_path}...")

    if not os.path.exists(db_path):
        print("Error: File with database is not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        

        query = "SELECT * FROM events LIMIT 5"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            print("Table is empty.")
        else:
            print(df)
            print(f"\nTotal rows: {len(df)}")
            
    except Exception as e:
        print(f"Error while reading: {e}")

if __name__ == "__main__":
    check_data()