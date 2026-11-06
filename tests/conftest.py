from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from booking.app import create_app
from booking.config import Settings

TEST_DATABASE_URL = "postgresql://test:test@localhost:5432/test"


@pytest.fixture
def settings() -> Settings:
    return Settings(
        environment="test",
        log_level="warning",
        app_version="0.0.0-test",
        database_url=TEST_DATABASE_URL,  # type: ignore
    )


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(settings=settings)) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def _clean_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for name in Settings.model_fields:
        monkeypatch.delenv(name.upper(), raising=False)
    monkeypatch.chdir(tmp_path)
