import typing
import uuid

import requests
import backend


def download_url(
    url: str, save_directory: str, error_directory: str
) -> typing.Tuple[bool, str]:
    url_uuid = uuid.uuid1()
    download_success = False
    try:
        r = requests.get(url)
        if r.status_code == 200:
            download_success = True
    except Exception as e:
        print(e)
    if download_success:
        filepath = f"{save_directory}/{url_uuid}"
        open(filepath, "wb").write(r.content)
    else:
        filepath = f"{error_directory}/{url_uuid}"
        open(filepath, "w").write("")
    return download_success, filepath


def download_urls(**context):
    generated_urls = context["task_instance"].xcom_pull(task_ids="generate_url")
    downloaded_files = []
    for url in generated_urls:
        success, result_filepath = download_url(
            url=url.strip(),
            save_directory=backend.BACKEND_DOWNLOAD_DIRECTORY,
            error_directory=backend.BACKEND_ERROR_DIRECTORY,
        )
        downloaded_files.append(
            {"success": success, "url": url, "filepath": result_filepath}
        )
    return downloaded_files
