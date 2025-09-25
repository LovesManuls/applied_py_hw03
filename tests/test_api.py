import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.main import app

client = TestClient(app)

@pytest.mark.parametrize("short_code, status_code", [
    ("OuZUgt", 200),  # for now it exists
    ("zNfojq", 200),  # for now it exists
    ("fdrdff", 404),  # not exists
    ("OuZUgtt", 404),  # not exists
])
def test_get_orig_link(short_code : str, status_code : int):
    response = client.get(f"/links/{short_code}")
    assert response.status_code == status_code


@pytest.mark.parametrize("short_code, status_code", [
    ("OuZUgt", 200),  # for now it exists
    ("zNfojq", 200),  # for now it exists
])
def test_get_stats(short_code : str, status_code : int):
    response = client.get(f"/links/{short_code}/stats")
    assert response.status_code == status_code


@pytest.mark.parametrize("orig_code, status_code", [
    ("https://www.wikipedia.org/", 200),  # for now it exists
    ("t43jkojk43", 404),  # not exists
])
def test_search_by_orig_link(orig_code : str, status_code : int):
    response = client.get(f"/links/{orig_code}/stats")
    assert response.status_code == status_code
