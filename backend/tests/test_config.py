import pytest

from caseflow.core.config import Settings


def test_database_url_can_be_overridden_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = (
        "postgresql+psycopg://test_user:test_password@localhost:5432/test_caseflow"
    )

    monkeypatch.setenv("CASEFLOW_DATABASE_URL", database_url)

    settings = Settings()

    assert settings.database_url == database_url
