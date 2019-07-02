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


def parse_url_file(url_filepath: str, limit: typing.Union[int,str] = 20):
    count = 0
    limit=int(limit)
    downloaded_files = []
    with open(url_filepath, "r") as url_file:
        for url in url_file:
            success, result_filepath = download_url(
                url=url.strip(),
                save_directory=backend.BACKEND_DOWNLOAD_DIRECTORY,
                error_directory=backend.BACKEND_ERROR_DIRECTORY,
            )
            downloaded_files.append(
                {"success": success, "url": url, "filepath": result_filepath}
            )
            count += 1
            if count == limit:
                break
    return downloaded_files


if __name__ == "__main__":
    parse_url_file(url_filepath="urls.txt")
