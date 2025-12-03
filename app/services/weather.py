from __future__ import annotations
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any
import requests
from flask import current_app
from ..extensions import db
from ..models import WeatherCache
import hashlib


@dataclass
class WeatherSlice:
    label: str
    icon: str
    summary: str
    temp_c: float | None = None


WEATHER_CODE_MAP = {
    # Simplified mapping for MVP
    0: ("sun", "Clear"),
    1: ("sun", "Mainly clear"),
    2: ("cloud", "Partly cloudy"),
    3: ("clouds", "Overcast"),
    45: ("cloud-fog", "Fog"),
    48: ("cloud-fog", "Rime fog"),
    51: ("cloud-drizzle", "Light drizzle"),
    53: ("cloud-drizzle", "Drizzle"),
    55: ("cloud-drizzle", "Heavy drizzle"),
    61: ("cloud-rain", "Light rain"),
    63: ("cloud-rain", "Rain"),
    65: ("cloud-rain", "Heavy rain"),
    71: ("cloud-snow", "Snow"),
    80: ("cloud-rain", "Rain showers"),
    95: ("cloud-lightning", "Thunderstorm"),
}


def _decode(code: int) -> tuple[str, str]:
    return WEATHER_CODE_MAP.get(code, ("cloud", "Weather"))


def _slots(now: datetime) -> Dict[str, int]:
    # Return representative hours for morning, noon, afternoon
    return {"morning": 9, "noon": 12, "afternoon": 15}


def fetch_open_meteo(lat: float, lon: float, tz: str) -> Dict[str, WeatherSlice]:
    if lat is None or lon is None:
        return {
            "morning": WeatherSlice("Morning", "cloud", "Set location"),
            "noon": WeatherSlice("Noon", "cloud", "Set location"),
            "afternoon": WeatherSlice("Afternoon", "cloud", "Set location"),
        }
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,weathercode",
        "timezone": tz or "UTC",
    }
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception:
        # Graceful fallback if network/API fails
        return {
            "morning": WeatherSlice("Morning", "cloud", "Unavailable"),
            "noon": WeatherSlice("Noon", "cloud", "Unavailable"),
            "afternoon": WeatherSlice("Afternoon", "cloud", "Unavailable"),
        }
    hours = data.get("hourly", {})
    times = hours.get("time", [])
    temps = hours.get("temperature_2m", [])
    codes = hours.get("weathercode", [])

    now = datetime.now()
    slot_hours = _slots(now)
    out: Dict[str, WeatherSlice] = {}
    for key, hour in slot_hours.items():
        # find index for today's date at desired hour
        target_prefix = now.strftime("%Y-%m-%dT") + f"{hour:02d}:00"
        try:
            idx = times.index(target_prefix)
            code = int(codes[idx]) if idx < len(codes) else 0
            temp = float(temps[idx]) if idx < len(temps) else None
        except ValueError:
            code, temp = 0, None
        icon, summary = _decode(code)
        out[key] = WeatherSlice(key.capitalize(), icon, summary, temp)
    return out


def get_weather(lat: float, lon: float, tz: str) -> Dict[str, Any]:
    # Cache by location+timezone+date using md5 to fit 32-char column
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if lat is None or lon is None:
        cache_key = today  # do not lock cache to empty location; will avoid persisting below
    else:
        raw = f"{round(lat,4)},{round(lon,4)},{tz or 'UTC'},{today}"
        cache_key = hashlib.md5(raw.encode("utf-8")).hexdigest()
    ttl_minutes = int(current_app.config.get("WEATHER_TTL_MINUTES", 60))
    cache: WeatherCache | None = WeatherCache.query.filter_by(date_key=cache_key).first()
    if cache and cache.fetched_at and (datetime.utcnow() - cache.fetched_at) < timedelta(minutes=ttl_minutes):
        try:
            result = {
                "morning": json.loads(cache.morning_json) if cache.morning_json else None,
                "noon": json.loads(cache.noon_json) if cache.noon_json else None,
                "afternoon": json.loads(cache.afternoon_json) if cache.afternoon_json else None,
            }
            # Convert old temp_c to temp_f if needed (backward compatibility)
            for key in ["morning", "noon", "afternoon"]:
                if result[key] and "temp_c" in result[key] and "temp_f" not in result[key]:
                    if result[key]["temp_c"] is not None:
                        result[key]["temp_f"] = round(result[key]["temp_c"] * 9 / 5 + 32, 1)
                    else:
                        result[key]["temp_f"] = None
            return result
        except Exception:
            pass
    slices = fetch_open_meteo(lat, lon, tz)
    # Convert Celsius to Fahrenheit: F = C * 9/5 + 32
    payload = {
        k: {
            "label": v.label,
            "icon": v.icon,
            "summary": v.summary,
            "temp_f": round(v.temp_c * 9 / 5 + 32, 1) if v.temp_c is not None else None,
        }
        for k, v in slices.items()
    }
    # Only persist cache when we have a location
    if lat is not None and lon is not None:
        if not cache:
            cache = WeatherCache(date_key=cache_key)
            db.session.add(cache)
        cache.morning_json = json.dumps(payload.get("morning"))
        cache.noon_json = json.dumps(payload.get("noon"))
        cache.afternoon_json = json.dumps(payload.get("afternoon"))
        cache.fetched_at = datetime.utcnow()
        db.session.commit()
    return payload


