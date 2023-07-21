import pendulum
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from backend import download, generate, grayscale, load_result, md5, update_monitoring


dag = DAG(
    "main_dag",
    description="Simple example DAG",
    # run every minutes
    schedule_interval="*/5 * * * *",
    start_date=pendulum.datetime(2017, 3, 20),
    # workflow can be run in parralel
    concurrency=3,
    catchup=False,
)

generate_url = PythonOperator(
    task_id="generate_url",
    python_callable=generate.generate_urls,
    dag=dag,
)


download_image = PythonOperator(

    task_id="download_image",
    python_callable=download.download_urls,
    dag=dag,
    provide_context=True,
)

md5_image = PythonOperator(
    task_id="md5_image",
    python_callable=md5.md5,
    dag=dag,
    provide_context=True,
)

grayscale_image = PythonOperator(
    task_id="grayscale_image",
    python_callable=grayscale.grayscale,
    dag=dag,
    provide_context=True,
)

load_result_image = PythonOperator(
    task_id="load_result_image",
    python_callable=load_result.load_result,
    dag=dag,
    provide_context=True,
)

update_monitoring_image = PythonOperator(
    task_id="update_monitoring_image",
    python_callable=update_monitoring.update_monitoring,
    op_kwargs={"url_filepath": "/opt/backend/urls.txt"},
    dag=dag,
    provide_context=True,
)

generate_url >> download_image
download_image >> md5_image >> load_result_image
download_image >> grayscale_image >> load_result_image
load_result_image >> update_monitoring_image
