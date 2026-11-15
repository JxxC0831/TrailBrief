from datetime import date, timedelta
from fastapi import APIRouter, HTTPException, Query
from app.api.schemas import WeatherResponse
from app.providers.nws_weather import fetch

router = APIRouter(prefix = "/api/v1", tags = ["weather"])

MAX_DAYS_AHEAD = 6

def _today() -> date:
    return date.today()

@router.get("/weather", response_model = WeatherResponse)
def get_weather(
    lat: float = Query(..., ge = -90, le = 90),
    lon: float = Query(..., ge = -180, le = 180),
    target_date: date = Query(..., alias = "date"),
):
    today = _today()
    if not(today <= target_date <= today + timedelta(days = MAX_DAYS_AHEAD)):
        raise HTTPException(
            status_code = 422, 
            detail = f"date must be between {today} and {today + timedelta(days = MAX_DAYS_AHEAD)}")
    return fetch(lat, lon, target_date)

