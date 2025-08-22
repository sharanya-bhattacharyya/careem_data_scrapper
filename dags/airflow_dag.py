from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="careem_scraper_dag",
    default_args=default_args,
    description="Run Careem UAE Promotional Scraper",
    schedule_interval=None,  # Set to desired schedule, e.g., '@daily'
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["careem", "scraper"],
) as dag:

    run_scraper = BashOperator(
        task_id="run_careem_scraper",
        bash_command="python3 /Users/jijobhattacharyya/assignment/careem_scraper.py",
        cwd="/Users/jijobhattacharyya/assignment",
    )