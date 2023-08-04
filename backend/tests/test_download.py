from turtle import width
import uuid
from requests import HTTPError
from backend.download import download_url, download_urls
from unittest.mock import MagicMock
from models.url import UrlPicsum
from models.image import PartialImage
from models.event import Event, EventStatus


def test_download_url(mocker):
    expected_uuid = uuid.uuid1()
    expected_image = b"truc"
    mocker.patch("backend.download.uuid.uuid1", MagicMock(return_value=expected_uuid))
    mocker.patch(
        "backend.download.requests.get", return_value=MagicMock(content=expected_image)
    )
    result_event, result_partial_image = download_url(
        UrlPicsum(url="http://fake_urls.com/", width=1, height=1)
    )
    assert expected_uuid == result_event.id
    assert EventStatus.SUCCESS == result_event.status
    assert expected_image == result_partial_image.content


def test_download_url_fail_exception(mocker):
    expected_uuid = uuid.uuid1()
    mocker.patch("backend.download.uuid.uuid1", MagicMock(return_value=expected_uuid))
    mocker.patch("backend.download.requests.get", side_effect=HTTPError())
    result_event, result_partial_image = download_url(
        UrlPicsum(url="http://fake_urls.com", width=1, height=1)
    )
    assert expected_uuid == result_event.id
    assert EventStatus.ERROR == result_event.status
    assert result_partial_image is None


def test_download_urls(mocker):
    expected_url_uuid = uuid.uuid1()
    expected_url = UrlPicsum(url="http://fake_urls.com/", width=1, height=1)
    expected_status = EventStatus.SUCCESS
    expected_image = b"truc"
    mocker.patch(
        "backend.download.download_url",
        return_value=(
            Event(
                id=expected_url_uuid, url=str(expected_url.url), status=expected_status
            ),
            PartialImage(event_id=expected_url_uuid, content=expected_image),
        ),
    )
    mocker.patch("backend.download.create_event", return_value=MagicMock())
    mocker.patch("backend.download.upsert_partial_image", return_value=MagicMock())
    results = download_urls([UrlPicsum(url="http://fake_urls.com", width=1, height=1)])
    assert 1 == len(results)
