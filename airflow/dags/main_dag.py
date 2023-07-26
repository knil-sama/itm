import pendulum

from airflow import DAG
from airflow.decorators import task
from backend import (
    download,
    generate,
    grayscale,
    load_result,
    md5,
    update_monitoring,
)

with DAG(
    "main_dag",
    # run every 5 minutes
    schedule_interval="*/5 * * * *",
    start_date=pendulum.datetime(2017, 3, 20),
    # workflow can be run in parralel
    concurrency=3,
    catchup=False,
) as dag:

    @task
    def generate_urls() -> list[str]:
        return generate.generate_urls()

    @task
    def download_image(generated_urls: list[str]) -> list[dict]:
        return download.download_urls(generated_urls)

    @task
    def md5_image(downloaded_images: list[dict]) -> None:
        return md5.md5(downloaded_images)

    @task
    def grayscale_image(downloaded_images: list[dict]) -> None:
        return grayscale.grayscale(downloaded_images)

    @task
    def load_result_image(downloaded_images: list[dict], *_) -> None:  # noqa: ANN002
        return load_result.load_result(downloaded_images)

    @task
    def update_monitoring_image(
        downloaded_images: list[dict],
        _,  # noqa: ANN001
    ) -> None:
        execution_date = "{{ dag_run.logical_date }}"
        return update_monitoring.update_monitoring(downloaded_images, execution_date)

    task_download_image = download_image(generate_urls())
    task_md5 = md5_image(task_download_image)
    task_grayscale = grayscale_image(task_download_image)
    task_load = load_result_image(task_download_image, task_md5, task_grayscale)
    update_monitoring_image(task_download_image, task_load)
