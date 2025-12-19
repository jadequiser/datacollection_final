from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 1),
    'retries': 0,
}

with DAG(
    'job3_daily_analytics',
    default_args=default_args,
    description='DAG 3: Bash Execution',
    schedule='@daily',
    catchup=False,
    tags=['project', 'analytics']
) as dag:

    t1 = BashOperator(
        task_id='calculate_analytics',
        bash_command="cd /opt/airflow/src && python job3_analytics.py"
    )