import httpx
import re

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

    