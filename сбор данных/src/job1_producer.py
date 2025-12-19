import json
import requests
import time
import os
from kafka import KafkaProducer

def fetch_and_produce_messages():
    print("DAG1")
    
    try:
        kafka_bootstrap = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
        producer = KafkaProducer(
            bootstrap_servers=[kafka_bootstrap],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        print("Kafka Producer connected.")
    except Exception as e:
        print(f"Could not connect to Kafka: {e}")
        return

    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    
    try:
        response = requests.get(url)
        data = response.json()
        features = data.get('features', [])
        
        print(f"Received events from API: {len(features)}")
        
        if not features:
            print("No earthquakes in the last hour.")
            return

        topic_name = 'earthquake_data'
        
        for feature in features:
            producer.send(topic_name, value=feature)
        
        producer.flush() 
        print(f"Success: {len(features)} messages sent to topic:'{topic_name}'.")
        
        producer.close()
        
    except Exception as e:
        print(f"Error sending: {e}")

if __name__ == "__main__":
    fetch_and_produce_messages()