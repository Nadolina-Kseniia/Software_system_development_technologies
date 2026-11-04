import pytest
from fastapi.testclient import TestClient

PAYLOAD = {
    "seat_id": "desk-1",
    "user_id": "u-1",
    "starts_at": "2030-10-14T09:00:00Z",
    "ends_at": "2030-10-14T12:00:00Z",
}


def test_booking_is_created(client: TestClient) -> None:
    response = client.post("/bookings", json=PAYLOAD)
    assert response.status_code == 201
    assert response.json()["seat_id"] == "desk-1"


def test_overlapping_booking_is_rejected(client: TestClient) -> None:
    client.post("/bookings", json=PAYLOAD)
    response = client.post("/bookings", json=PAYLOAD)
    assert response.status_code == 409


@pytest.mark.parametrize(
    ("starts_at", "ends_at"),
    [
        ("2030-10-14T12:00:00Z", "2030-10-14T09:00:00Z"),  # end before start
        ("2030-10-14T09:00:00Z", "2030-10-14T09:00:00Z"),  # zero length
    ],
)
def test_invalid_interval_is_rejected(client: TestClient, starts_at: str, ends_at: str) -> None:
    payload = {**PAYLOAD, "starts_at": starts_at, "ends_at": ends_at}
    response = client.post("/bookings", json=payload)
    assert response.status_code == 422
