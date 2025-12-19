import pandas as pd
import sqlite3
import os

def calculate_daily_analytics():
    print("DAG3")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"Database is not found by {db_path} path")
        return

    try:
        conn = sqlite3.connect(db_path)
        
        df = pd.read_sql_query("SELECT * FROM events", conn)
        
        if df.empty:
            print("No data found.")
            conn.close()
            return

        print(f"Downloaded {len(df)} rows.")

        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['date'] = df['time'].dt.date

        summary = df.groupby('date').agg(
            total_events=('id', 'count'),    
            avg_magnitude=('mag', 'mean'), 
            max_magnitude=('mag', 'max')   
        ).reset_index()

        summary['avg_magnitude'] = summary['avg_magnitude'].round(2)

        print("Stats:")
        print(summary)

        summary.to_sql('daily_summary', conn, if_exists='replace', index=False)
        print("Stats saved to 'daily_summary' table.")
        
        conn.close()

    except Exception as e:
        print(f"Analytics Error: {e}")

if __name__ == "__main__":
    calculate_daily_analytics()