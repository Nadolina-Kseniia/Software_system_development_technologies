from fastapi.testclient import TestClient

from booking.api.middleware import REQUEST_ID_HEADER


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_reports_configured_version(client: TestClient) -> None:
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.0-test", "environment": "test"}


def test_request_id_is_returned(client: TestClient) -> None:
    response = client.get("/health")
    assert response.headers[REQUEST_ID_HEADER]
