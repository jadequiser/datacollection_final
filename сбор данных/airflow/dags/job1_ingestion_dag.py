import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


sys.path.append('/opt/airflow/src') 
from job1_producer import fetch_and_produce_messages

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 1),
    'retries': 0,
}

with DAG(
    'job1_continuous_ingestion',
    default_args=default_args,
    description='DAG 1: Python Execution',
    schedule=timedelta(minutes=1),
    catchup=False,
    tags=['project', 'earthquake']
) as dag:

    t1 = PythonOperator(
        task_id='fetch_earthquake_data',
        python_callable=fetch_and_produce_messages
    )