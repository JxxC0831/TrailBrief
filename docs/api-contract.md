# API Contract — v1

## GET /api/v1/weather

Returns hourly NWS forecast for one location on one local date.

### Query parameters

| Param | Type | Required | Constraint | Example |
|---|---|---|---|---|
| lat | float | yes | -90 ≤ lat ≤ 90 | 34.1184 |
| lon | float | yes | -180 ≤ lon ≤ 180 | -118.3004 |
| date | string | yes | YYYY-MM-DD; today ≤ date ≤ today + 6 days | 2026-11-15 |

Invalid input → HTTP 422 with FastAPI's default error body.

### Response — 200

Envelope (same shape for every provider):

| Field | Type | Description |
|---|---|---|
| provider | string | always `"nws_hourly"` |
| status | `"ok"` \| `"no_data"` \| `"unavailable"` | see below |
| fetched_at | ISO 8601 UTC | when TrailBrief called NWS |
| source_url | string | the forecastHourly URL actually fetched |
| valid_for | YYYY-MM-DD | the requested local date |
| data | HourlyWeather[] \| null | null unless status is ok |
| error_code | string \| null | null when status is ok |

`HourlyWeather`:

| Field | Type | Nullable | Source |
|---|---|---|---|
| time | ISO 8601 with local offset | no | startTime |
| temp_f | int | no | temperature (converted if unit is C) |
| wind_mph | int | yes | windSpeed, upper bound of range, calm -> 0, for rule evaluation|
| wind_text | string | yes | windSpeed, verbatim (e.g. "5 to 10 mph"); for display only|
| wind_dir | string | yes | windDirection |
| precip_pct | int | yes | probabilityOfPrecipitation.value |
| humidity_pct | int | yes | relativeHumidity.value |
| short_forecast | string | no | shortForecast |

### Status and error codes

| status | error_code | When |
|---|---|---|
| ok | null | ≥1 hour matched the date |
| no_data | outside_forecast_range | NWS responded but no hours fall on that date |
| no_data | malformed_response | missing keys / empty periods |
| unavailable | upstream_timeout | NWS did not answer in 10 s |
| unavailable | upstream_http_error | NWS returned 4xx/5xx |
| unavailable | upstream_unreachable | network error |

Upstream failures still return HTTP 200 with status ≠ ok; only bad input returns 4xx.

### Example

GET /api/v1/weather?lat=34.1184&lon=-118.3004&date=2026-11-15

(paste one real abbreviated response here once the endpoint works)