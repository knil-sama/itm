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
from models.event import Event
from models.url import UrlPicsum

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
        return [
            url.json() for url in generate.generate_urls()
        ]  # should use model_dump_json() in v2

    @task
    def download_image(generated_urls: list[str]) -> list[str]:
        pydantic_generated_urls = [UrlPicsum.parse_raw(url) for url in generated_urls]
        return [
            event.json() for event in download.download_urls(pydantic_generated_urls)
        ]  # should use model_dump_json() in v2

    @task
    def md5_image(events: list[str]) -> None:
        pydantic_events = [Event.parse_raw(event) for event in events]
        return md5.md5(pydantic_events)

    @task
    def grayscale_image(events: list[str]) -> None:
        pydantic_events = [Event.parse_raw(event) for event in events]
        return grayscale.grayscale(pydantic_events)

    @task
    def load_result_image(events: list[str], *_) -> None:  # noqa: ANN002
        pydantic_events = [Event.parse_raw(event) for event in events]
        return load_result.load_result(pydantic_events)

    @task
    def update_monitoring_image(
        events: list[str],
        _,  # noqa: ANN001
    ) -> None:
        execution_date = "{{ dag_run.logical_date }}"
        pydantic_events = [Event.parse_raw(event) for event in events]
        return update_monitoring.update_monitoring(pydantic_events, execution_date)

    task_download_image = download_image(generate_urls())
    task_md5 = md5_image(task_download_image)
    task_grayscale = grayscale_image(task_download_image)
    task_load = load_result_image(task_download_image, task_md5, task_grayscale)
    update_monitoring_image(task_download_image, task_load)
