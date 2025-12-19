import sqlalchemy
from sqlalchemy import create_engine, text

import os

DB_NAME = 'app.db'
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '..', 'data', DB_NAME)
DB_CONNECTION_URL = f"sqlite:///{db_path}"

def get_db_engine():
    engine = create_engine(DB_CONNECTION_URL)
    return engine

def init_db():
    engine = get_db_engine()
    
    create_events_table = """
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        place TEXT,
        time DATETIME,
        magnitude REAL,
        type TEXT,
        latitude REAL,
        longitude REAL,
        depth REAL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_summary_table = """
    CREATE TABLE IF NOT EXISTS daily_summary (
        date DATE PRIMARY KEY,
        total_events INTEGER,
        avg_magnitude REAL,
        max_magnitude REAL,
        top_place TEXT
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(create_events_table))
        conn.execute(text(create_summary_table))
        print("Database is successfully initiated.")

if __name__ == "__main__":
    init_db()