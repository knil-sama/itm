from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import backend.download as download
import backend.md5 as md5
import backend.grayscale as grayscale
import backend.load_result as load_result
import backend.update_monitoring as update_monitoring

dag = DAG(
    "main_dag",
    description="Simple example DAG",
    # run every minutes 
    schedule_interval="* * * * *",
    start_date=datetime(2017, 3, 20),
    # workflow is not supposed to be run in parralel
    concurrency=1,
    catchup=False,
)

download_operator = PythonOperator(
    task_id="download_image",
    python_callable=download.parse_url_file,
    op_kwargs={"url_filepath": "/opt/backend/urls.txt","limit": "10"},
    dag=dag,
)

md5_operator = PythonOperator(
    task_id="md5_image", python_callable=md5.md5, dag=dag, provide_context=True
)

grayscale_operator = PythonOperator(
    task_id="grayscale_image",
    python_callable=grayscale.grayscale,
    dag=dag,
    provide_context=True,
)

load_result_operator = PythonOperator(
    task_id="load_result_image",
    python_callable=load_result.load_result,
    dag=dag,
    provide_context=True,
)

update_monitoring_operator = PythonOperator(
    task_id="update_monitoring_image",
    python_callable=update_monitoring.update_monitoring,
    op_kwargs={"url_filepath": "/opt/backend/urls.txt"},
    dag=dag,
    provide_context=True,
)

download_operator >> md5_operator >> load_result_operator
download_operator >> grayscale_operator >> load_result_operator
load_result_operator >> update_monitoring_operator
