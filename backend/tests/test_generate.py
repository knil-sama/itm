from backend.generate import generate_url, generate_urls
from models.url import Url
import pytest


def test_generate_url():
    assert isinstance(generate_url(), Url)


def test_generate_urls():
    assert 1 == len(generate_urls(1, 1))
    random_len = len(generate_urls(1, 10))
    assert random_len <= 10
    assert random_len >= 1


def test_generate_urls_fail_when_min_over_max():
    with pytest.raises(ValueError):
        generate_urls(4, 2)


def test_generate_urls_fail_when_min_or_max_is_lower_than_1():
    with pytest.raises(ValueError):
        generate_urls(0, 1)
    with pytest.raises(ValueError):
        generate_urls(1, 0)
