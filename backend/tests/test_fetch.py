from app.providers.nws_weather import fetch
from datetime import date
import json
from tests.conftest import FIXTURES


def fake_get_json(client, url):
    if "/points/" in url:
        return json.load(open(FIXTURES / "points_griffith.json"))
    return json.load(open(FIXTURES / "hourly_griffith.json"))

def test_fetch_ok(monkeypatch):
    monkeypatch.setattr("app.providers.nws_weather._get_json", fake_get_json)
    r = fetch(34.1184, -118.3004, date(2026,11,13))
    assert r["status"] == "ok"
    assert len(r["data"]) == 24

def test_fetch_upstream_timeout(monkeypatch):
    monkeypatch.setattr("app.providers.nws_weather._get_json", lambda client, url: "upstream_timeout")
    r = fetch(34.1184, -118.3004, date(2026, 11, 13))
    assert r["status"] == "unavailable"
    assert r["error_code"] == "upstream_timeout"
    assert r["data"] is None

def test_fetch_outside_forecast_range(monkeypatch):
    monkeypatch.setattr("app.providers.nws_weather._get_json", fake_get_json)
    r = fetch(34.1184, -118.3004, date(2027, 1, 1))
    assert r["status"] == "no_data"
    assert r["error_code"] == "outside_forecast_range"

def test_fetch_null_precip_preserved(monkeypatch):
    def fake_with_null(client, url):
        data = fake_get_json(client, url)
        if "/points/" not in url:
            data["properties"]["periods"][0]["probabilityOfPrecipitation"]["value"] = None
        return data
    monkeypatch.setattr("app.providers.nws_weather._get_json", fake_with_null)
    r = fetch(34.1184, -118.3004, date(2026, 11, 12))  
    assert r["data"][0]["precip_pct"] is None