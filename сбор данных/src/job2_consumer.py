import json
import os
import pandas as pd
from kafka import KafkaConsumer
from sqlalchemy import text
from db_utils import get_db_engine
import datetime

def run_consumer():
    TOPIC_NAME = 'earthquake_data'
    kafka_bootstrap = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
    BOOTSTRAP_SERVERS = [kafka_bootstrap]
    
    engine = get_db_engine()
    print("Database checking...")
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                place TEXT,
                mag REAL,
                time DATETIME
            )
        """))
    print("Table is ready.")
    

    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='batch_consumer_group_pandas_v2', 
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=10000 
    )

    print("Job 2: Starting reading from Kafka (Batch)...")


    raw_messages = []
    
    for message in consumer:
        data = message.value
        props = data.get('properties', data)
        
        row = {
            'id': data.get('id', props.get('id')),
            'place': props.get('place'),
            'mag': props.get('mag'),
            'time': props.get('time')
        }
        raw_messages.append(row)

    if not raw_messages:
        print("No new data from Kafka. Finishing work.")
        return

    print(f"Downloaded {len(raw_messages)} raw data. Starting cleaning Pandas...")

    df = pd.DataFrame(raw_messages)

    df = df.dropna(subset=['id', 'mag', 'time'])

    df['time'] = pd.to_datetime(df['time'], unit='ms')

    df = df[df['mag'] >= 0]

    if 'place' in df.columns:
        df['place'] = df['place'].str.strip()

    print(f"Data is cleaned. Rows left: {len(df)}")

    count = 0
    with engine.begin() as conn:
        for index, row in df.iterrows():
            try:
                clean_time = row['time'].to_pydatetime()
                
                query = text("""
                    INSERT OR IGNORE INTO events (id, place, mag, time)
                    VALUES (:id, :place, :mag, :time)
                """)
                conn.execute(query, {
                    'id': row['id'],
                    'place': row['place'],
                    'mag': row['mag'],
                    'time': clean_time 
                })
                count += 1
            except Exception as e:
                print(f"Error ID pasting {row['id']}: {e}")

    print(f"Successfully processed: {len(df)} rows.")

if __name__ == "__main__":
    run_consumer()