import os
import uuid

import psycopg
import pytest
import requests


BASE_URL = os.getenv("BASE_URL", "http://localhost:8081")


@pytest.fixture
def db_connection():
    conn = psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
	port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "testdb"),
        user=os.getenv("DB_USER", "testuser"),
        password=os.getenv("DB_PASSWORD", "testpass"),
    )

    try:
        yield conn
    finally:
        conn.close()


def test_create_item_and_validate_database(db_connection):
    # Generate unique test data
    item_name = f"iPad-Pro-{uuid.uuid4().hex[:8]}"
    payload = {
        "name": item_name,
        "price": 999.99,
    }

    item_id = None

    try:
        # Step 1: Create item through API
        response = requests.post(
            f"{BASE_URL}/items",
            json=payload,
            timeout=10,
        )

        # Step 2: Validate API response
        assert response.status_code == 201

        data = response.json()
        item_id = data["id"]

        assert data["name"] == payload["name"]
        assert data["price"] == payload["price"]

        # Step 3: Query database directly
        row = db_connection.execute(
            "SELECT name, price FROM items WHERE id = %s",
            (item_id,),
        ).fetchone()

        # Step 4: Compare database against API
        assert row is not None
        assert row[0] == payload["name"]
        assert row[1] == pytest.approx(payload["price"])

        # Step 5: Validate GET endpoint
        get_response = requests.get(
            f"{BASE_URL}/items/{item_id}",
            timeout=10,
        )

        assert get_response.status_code == 200
        assert get_response.json()["name"] == item_name

    finally:
        # Clean up test data even if an assertion fails
        if item_id is not None:
            db_connection.execute(
                "DELETE FROM items WHERE id = %s",
                (item_id,),
            )
            db_connection.commit()
def test_get_nonexistent_item():
    response = requests.get(
        f"{BASE_URL}/items/999999999",
        timeout=10
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_create_item_missing_name():
    payload = {"price": 99.99}

    response = requests.post(
        f"{BASE_URL}/items",
        json=payload,
        timeout=10
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "name"]
        for error in errors
    )
