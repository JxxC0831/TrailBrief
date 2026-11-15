import json
from app.providers.nws_weather import _normalize_period
from tests.conftest import FIXTURES

def _periods():
    with open(FIXTURES / "hourly_griffith.json") as f:
        return json.load(f)["properties"]["periods"]


def test_normalize_first_period_has_all_keys():
    row = _normalize_period(_periods()[0])
    assert set(row) == {"time", "temp_f", "wind_mph", "wind_text", "wind_dir",
                        "precip_pct", "humidity_pct", "short_forecast"}
    assert isinstance(row["precip_pct"], int)

def test_normalize_empty_wind_dir_becomes_none():
    p = next(p for p in _periods() if p["windDirection"] == "")
    row = _normalize_period(p)
    assert row["wind_dir"] is None
    assert row["wind_mph"] == 0
