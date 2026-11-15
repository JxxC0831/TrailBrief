from fastapi.testclient import TestClient
from app.main import app
from tests.test_fetch import fake_get_json
from datetime import date
client = TestClient(app)



def test_invalid_lat():
    r = client.get("/api/v1/weather", params = {"lat": 999, "lon": 0, "date": "2026-11-14"})
    assert r.status_code == 422

def test_date_out_of_range(monkeypatch):
    r = client.get("/api/v1/weather", params={"lat": 34.1, "lon": -118.3, "date": "2027-01-01"})
    monkeypatch.setattr("app.api.weather._today", lambda: date(2026, 11, 12))
    assert r.status_code == 422

def test_weather_ok(monkeypatch):
    monkeypatch.setattr("app.providers.nws_weather._get_json", fake_get_json)
    monkeypatch.setattr("app.api.weather._today", lambda: date(2026, 11, 12))
    r = client.get("/api/v1/weather", params={"lat": 34.1184, "lon": -118.3004, "date": "2026-11-13"})
    assert r.status_code == 200
    assert r.json()["status"] == "ok"