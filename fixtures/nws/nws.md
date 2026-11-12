# NWS fixtures

Captured 2026-11-12 for Griffith Observatory (34.1184, -118.3004).
captured 2026-11-12 for Mountain Baldy (34.2889, -117.6100)
Captured 2026-11-12 for Joshua Tree (33.8819, -115.9007)

| file | command |
| --- | --- |

# griffith.json
| points_griffith.json | `curl -s -H "User-Agent: TrailBrief (jaypersonal2001@gmail.com)" https://api.weather.gov/points/34.1184,-118.3004` |
| hourly_griffith.json | `curl -s -H "User-Agent: TrailBrief (jaypersonal2001@gmail.com)" https://api.weather.gov/gridpoints/LOX/154,48/forecast/hourly` |

# baldy.json
| points_baldy.json | `curl -s -H "User-Agent: TrailBrief (jaypersonal2001@gmail.com)" https://api.weather.gov/points/34.2889,-117.6100` |
| hourly_baldy.json | `curl -s -H "User-Agent: TrailBrief (jaypersonal2001@gmail.com)" https://api.weather.gov/gridpoints/SGX/52,85/forecast/hourly` |

# joshuatree.json
| points_joshuatree.json | `curl -s -H "User-Agent: TrailBrief (jaypersonal2001@gmail.com)" https://api.weather.gov/points/33.8819,-115.9007` |
| hourly_joshuatree.json | `curl -s -H "User-Agent: TrailBrief (jaypersonal2001@gmail.com)" https://api.weather.gov/gridpoints/PSR/22,97/forecast/hourly` |