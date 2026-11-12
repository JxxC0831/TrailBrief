# Data Sources

## Test destinations

| Name | Lat, Lon | Verified via | NWS gridId / X,Y | NWS timeZone | Notes |
|---|---|---|---|---|---|
| Griffith Observatory | 34.1184, -118.3004 | Google Maps, 2026-11-12 | LOX / 154,48 | America/Los_Angeles | urban, ~300 m, level easy |
| Mt. Baldy | 34.2889, -117.61 | Google arcgis storymap, 2026-11-12| SGX / 52,85 | America/Los_Angeles | alpine, ~1900 m start, level hard|
| Joshua Tree | 33.8819, -115.9007 | Google latlong.net, 2026-11-12 | PSR / 22,97 | America/Los_Angeles | desert, large diurnal swing, level medium, ~1270m |

## NWS (National Weather Service)

- Base: https://api.weather.gov
- Auth: none. Requires `User-Agent: TrailBrief (<email>)`.
- Flow: `GET /points/{lat},{lon}` → `properties.forecastHourly` → `GET` that URL → `properties.periods[]`.
- Coverage: ~156 hours ahead, hourly.
- Fixtures: `fixtures/nws/points_<place>.json`, `fixtures/nws/hourly_<place>.json`, captured 2026-11-12.
- three points fall in three forecast offices (LOX / SGX / PSR); grid mapping is not something we compute, always obtained from /points.

### Fields used from `periods[]`

| NWS field | Type | Nullable | Mapped to |
|---|---|---|---|
| startTime | ISO 8601 with offset | no | time |
| temperature + temperatureUnit | int + "F" | no | temp_f |
| windSpeed | string, e.g. "5 mph". NWS also emits a range form "5 to 10 mph" (seen in docs, not in 2026-11-12 fixtures); parser must handle both | no | wind_mph |
| windDirection | string | yes - empty string when 0 mph | wind_dir |
| probabilityOfPrecipitation.value | int | **yes** | precip_pct |
| relativeHumidity.value | int | no | humidity_pct |
| shortForecast | string | no | short_forecast |

### Known pitfalls

- if coordinates with more than 4 decimals, we might have empty response, so we need to round lat and lon first.
- precip is null does not means 0. probabilityOfPrecipitation.value is null means there is no data at nws. Use none instead. 
- filter by local date, not UTC
- NWS returns 404 for points outside its coverage (ocean, Mexico); provider maps this to upstream_http_error
