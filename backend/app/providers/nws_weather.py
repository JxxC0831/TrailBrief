import httpx
import re
from datetime import date as Date, datetime, timezone

USER_AGENT = "TrailBrief (jaypersonal2001@gmail.com)"

def _get_json(client: httpx.Client, url: str) -> dict | str:
    """Get JSON data from URL, if successful, return dict, otherwise return error_code"""
    try:
        response = client.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        return "upstream_timeout"
    except httpx.HTTPStatusError:
        return "upstream_http_error"
    except httpx.RequestError:
        return "upstream_unreachable"

def _parse_wind(s) -> int | None:
    """Parse wind string like '5 to 10 mph' or 'Calm' and return max wind speed in mph"""
    if not s: 
        return None
    nums = re.findall(r'\d+', s)
    if not nums:
        return 0 if 'calm' in s.lower() else None
    return max(int(n) for n in nums)

def _normalize_period(p: dict) -> dict:
    """one NWS period -> one HourlyWeather dict"""
    temp = p["temperature"]
    if p["temperatureUnit"] == "C":
        temp = round(temp * 9 / 5 + 32)

    return {
        "time": p["startTime"],
        "temp_f": temp,
        "wind_mph": _parse_wind(p["windSpeed"]),
        "wind_text": p.get("windSpeed"),
        "wind_dir": p.get("windDirection") or None ,
        "precip_pct": p.get("probabilityOfPrecipitation", {}).get("value"),
        "humidity_pct": p.get("relativeHumidity", {}).get("value"),
        "short_forecast": p["shortForecast"]
    }

def fetch(lat: float, lon: float, target: Date) -> dict:
    fetched_at =datetime.now(timezone.utc).isoformat()
    envelope = {"provider": "nws_hourly", "status": None, "fetched_at":fetched_at, "source_url": None, 
               "valid_for": target.isoformat(), "data": None, "error_code": None}

    with httpx.Client(timeout=10, headers={"User-Agent": USER_AGENT}) as client:
        points = _get_json(client, f"https://api.weather.gov/points/{round(lat,4)},{round(lon,4)}")
        if isinstance(points, str):
            envelope["status"] = "unavailable"
            envelope["error_code"] = points
            return envelope

        hourly_url = points.get("properties", {}).get("forecastHourly")
        if not hourly_url:
            envelope["status"] = "no_data"
            envelope["error_code"] = "malformed_response"
            return envelope
        
        envelope["source_url"] = hourly_url
        hourly =  _get_json(client, hourly_url)
        if isinstance(hourly, str):
            envelope["status"] = "unavailable"
            envelope["error_code"] = hourly
            return envelope

        periods = hourly.get("properties", {}).get("periods")
        if not periods:
            envelope["status"] = "no_data"
            envelope["error_code"] = "malformed_response"
            return envelope
        try: 
            rows = [ _normalize_period(p) for p in periods
                if datetime.fromisoformat(p["startTime"]).date() == target]
        except KeyError:
            envelope["status"] = "no_data"
            envelope["error_code"] = "malformed_response"
            return envelope

        if rows: 
            envelope["status"] = "ok"
            envelope["data"] = rows
        else:
            envelope["status"] = "no_data"
            envelope["error_code"] = "outside_forecast_range"
        return envelope