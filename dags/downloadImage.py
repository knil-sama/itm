from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from backend import download

dag = DAG(
    "download_image",
    description="Simple tutorial DAG",
    schedule_interval="0 12 * * *",
    start_date=datetime(2017, 3, 20),
    catchup=False,
)

download_operator = PythonOperator(
    task_id="download_image",
    python_callable=download.parse_url_file,
    op_kwargs={"url_filepath": "/opt/backend/urls.txt"},
    dag=dag,
)
