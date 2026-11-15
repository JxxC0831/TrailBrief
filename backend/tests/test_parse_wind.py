import pytest
from app.providers.nws_weather import _parse_wind

@pytest.mark.parametrize("raw, expected", [
    ("5 mph", 5),
    ("0 mph", 0),
    ("5 to 10 mph", 10),
    ("", None),
    (None, None),
    ("calm", 0),
])
def test_parse_wind(raw, expected):
    assert _parse_wind(raw) == expected

