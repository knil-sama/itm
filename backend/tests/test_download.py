from more_itertools import side_effect
from requests import HTTPError
from backend.download import download_url
from unittest.mock import MagicMock
import pathlib


def test_download_url(mocker, tmp_path):
    expected_uuid = "fake_uuid"
    expected_image = b"truc"
    mocker.patch("backend.download.uuid.uuid1", MagicMock(return_value=expected_uuid))
    mocker.patch(
        "backend.download.requests.get", return_value=MagicMock(content=expected_image)
    )
    returned_url_uuid, download_success, filepath = download_url(
        "fake_url", tmp_path, None
    )
    assert expected_uuid == returned_url_uuid
    assert True == download_success
    assert tmp_path / pathlib.Path(expected_uuid) == filepath
    assert expected_image == filepath.open("rb").read()


def test_download_url_fail_write_exception(mocker, tmp_path):
    expected_uuid = "fake_uuid"
    mocker.patch("backend.download.uuid.uuid1", MagicMock(return_value=expected_uuid))
    mocker.patch("backend.download.requests.get", side_effect=HTTPError())
    returned_url_uuid, download_success, filepath = download_url(
        "fake_url", None, tmp_path
    )
    assert expected_uuid == returned_url_uuid
    assert False == download_success
    assert tmp_path / pathlib.Path(expected_uuid) == filepath
