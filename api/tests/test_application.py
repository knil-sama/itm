from fastapi.testclient import TestClient
from polyfactory.factories.pydantic_factory import ModelFactory

from api.application import app
from models.image import Image
from models.monitoring import Monitoring
import pytest

client = TestClient(app)


class ImageFactory(ModelFactory[Image]):
    __model__ = Image


class MonitoringFactory(ModelFactory[Monitoring]):
    __model__ = Monitoring


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, this api exist to query data, see the docs/",
    }


def test_read_image(mocker):
    mock_image = ImageFactory.build()
    mocker.patch("api.application.get_image", return_value=mock_image)
    response = client.get("/image/fake_id")
    assert response.status_code == 200
    assert response.content.decode() == mock_image.grayscale


def test_read_image_not_found(mocker):
    mocker.patch("api.application.get_image", return_value=None)
    response = client.get("/image/fake_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Image fake_id not found"}


@pytest.mark.parametrize(
    "test_input",
    [
        [],
        [ImageFactory.build()],
        [ImageFactory.build(), ImageFactory.build(), ImageFactory.build()],
    ],
    ids=["empty", "1_element", "3_elements"],
)
def test_read_images(mocker, test_input):
    mocker.patch("api.application.get_images", return_value=test_input)
    response = client.get("/images/")
    assert response.status_code == 200
    assert response.json() == [input.id for input in test_input]


@pytest.mark.parametrize(
    "test_input",
    [
        [MonitoringFactory.build()],
        [
            MonitoringFactory.build(),
            MonitoringFactory.build(),
            MonitoringFactory.build(),
        ],
    ],
    ids=["1_element", "3_elements"],
)
def test_read_monitoring(mocker, test_input):
    mocker.patch("api.application.get_monitoring", return_value=test_input)
    response = client.get("/monitoring/")
    assert response.status_code == 200
    assert [item["success"] for item in response.json()] == [
        input.success for input in test_input
    ]
    assert [item["error"] for item in response.json()] == [
        input.error for input in test_input
    ]


def test_read_monitoring_empty(mocker):
    mocker.patch("api.application.get_monitoring", return_value=[])
    response = client.get("/monitoring/")
    assert response.status_code == 200
    assert response.json() == "Nothing to monitor yet"
