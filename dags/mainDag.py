from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import backend.download as download
import backend.md5 as md5

dag = DAG(
    "main_dag",
    description="Simple example DAG",
    schedule_interval="0 * * * *",
    start_date=datetime(2017, 3, 20),
    catchup=False,
)

download_operator = PythonOperator(
    task_id="download_image",
    python_callable=download.parse_url_file,
    op_kwargs={"url_filepath": "/opt/backend/urls.txt"},
    dag=dag,
)

md5_operator = PythonOperator(
    task_id="md5_image",
    python_callable=md5.md5,
    dag=dag,
    provide_context=True,
)

download_operator >> md5_operator
