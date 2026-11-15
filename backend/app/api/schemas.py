from pydantic import BaseModel
from typing import Literal
from datetime import date, datetime

class HourlyWeather(BaseModel):
    time: str
    temp_f: int
    wind_mph: int | None
    wind_text: str | None
    wind_dir: str | None
    precip_pct: int | None
    humidity_pct: int | None
    short_forecast: str

class WeatherResponse(BaseModel):
    provider: str
    status: Literal["ok", "no_data", "unavailable"]
    fetched_at: datetime
    source_url: str | None
    valid_for: date
    data: list[HourlyWeather] | None
    error_code: str | None

