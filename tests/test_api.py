
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_post_status_code():
    response = requests.get(
        f"{BASE_URL}/posts/1",
        timeout=10
    )

    assert response.status_code == 200


def test_get_post_response_data():
    response = requests.get(
        f"{BASE_URL}/posts/1",
        timeout=10
    )

    data = response.json()

    assert data["id"] == 1
    assert data["userId"] == 1
    assert "title" in data
    assert "body" in data


def test_get_missing_post():
    response = requests.get(
        f"{BASE_URL}/posts/999999",
        timeout=10
    )

    assert response.status_code == 404

