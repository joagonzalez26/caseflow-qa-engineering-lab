from fastapi.testclient import TestClient

from caseflow.main import app

client = TestClient(app)


def test_health_check_returns_service_status() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "CaseFlow API",
        "version": "0.1.0",
    }
