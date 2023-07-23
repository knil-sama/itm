from fastapi.testclient import TestClient
from polyfactory.factories.pydantic_factory import ModelFactory

from api.application import app
from models.image import Image

client = TestClient(app)


class ImageFactory(ModelFactory[Image]):
    __model__ = Image


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, this api exist to query data, see the docs/",
    }


def test_read_image(mocker):
    mock_image = ImageFactory.build()
    mocker.patch("api.application.get_image", return_value=mock_image)
    response = client.get("/image/fake_md5")
    assert response.status_code == 200
    assert response.content.decode() == mock_image.grayscale


def test_read_image_not_found(mocker):
    mocker.patch("api.application.get_image", return_value=None)
    response = client.get("/image/fake_md5")
    assert response.status_code == 404
    assert response.json() == {"detail": "Image fake_md5 not found"}
