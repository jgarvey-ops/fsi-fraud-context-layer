from fastapi.testclient import TestClient

from context_service.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_case_002():
    r = client.get("/v1/cases/CASE-002")
    assert r.status_code == 200
    body = r.json()
    assert body["case"]["case_id"] == "CASE-002"


def test_stream_injection_toggle():
    off = client.post("/v1/admin/stream/injection", json={"enabled": False})
    assert off.json()["stream_injection_enabled"] is False
    on = client.post("/v1/admin/stream/injection", json={"enabled": True})
    assert on.json()["stream_injection_enabled"] is True
    recent = client.get("/v1/stream/recent")
    assert len(recent.json()["events"]) >= 1
