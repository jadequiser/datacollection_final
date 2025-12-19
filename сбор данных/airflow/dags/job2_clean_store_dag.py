from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 1),
    'retries': 0,
}

with DAG(
    'job2_hourly_cleaning',
    default_args=default_args,
    description='DAG 2: Bash Execution',
    schedule='@hourly',
    catchup=False,
    tags=['project', 'cleaning']
) as dag:

    t1 = BashOperator(
        task_id='clean_and_store_data',
        bash_command="cd /opt/airflow/src && python job2_consumer.py"
    )