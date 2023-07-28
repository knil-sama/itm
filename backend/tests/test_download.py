import uuid
from requests import HTTPError
from backend.download import download_url, download_urls
from unittest.mock import MagicMock
from models.url import Url
from models.image import PartialImage
from models.event import Event, EventStatus


def test_download_url(mocker):
    expected_uuid = uuid.uuid1()
    expected_image = b"truc"
    mocker.patch("backend.download.uuid.uuid1", MagicMock(return_value=expected_uuid))
    mocker.patch(
        "backend.download.requests.get", return_value=MagicMock(content=expected_image)
    )
    result_event = download_url(Url(url="http://fake_urls.com"))
    assert expected_uuid == result_event.id
    assert EventStatus.SUCCESS == result_event.status


def test_download_url_fail_write_exception(mocker):
    expected_uuid = uuid.uuid1()
    mocker.patch("backend.download.uuid.uuid1", MagicMock(return_value=expected_uuid))
    mocker.patch("backend.download.requests.get", side_effect=HTTPError())
    result_event = download_url(Url(url="http://fake_urls.com"))
    assert expected_uuid == result_event.id
    assert EventStatus.ERROR == result_event.status


def test_download_urls(mocker, request):
    expected_url_uuid = uuid.uuid1()
    expected_url = Url(url="http://fake_urls.com")
    expected_status = EventStatus.SUCCESS
    expected_image = b"truc"
    mocker.patch(
        "backend.download.download_url",
        return_value=Event(
            id=expected_url_uuid,
            url=str(expected_url.url),
            status=expected_status,
            partial_image=PartialImage(content=expected_image),
        ),
    )
    mocker.patch("backend.download.load_event", return_value=MagicMock())
    results = download_urls([Url(url="http://fake_urls.com")])
    assert 1 == len(results)
