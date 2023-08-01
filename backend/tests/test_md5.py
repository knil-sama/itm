from backend.md5 import img_to_md5
from unittest.mock import MagicMock


def test_img_to_md5(mocker):
    assert "df7a140cd171b9e1b429c59b5cfc77cc" == img_to_md5(b"sfsfsdfsfsfd").id
