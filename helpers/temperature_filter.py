import bisect
from collections import defaultdict
from datetime import datetime
from typing import List
from dateutil import parser
import pytz

from models.forecast import TemperatureForecast


def to_timezone(utc_dt_str: str, tz_str: str) -> datetime:
    """Convert UTC datetime string to timezone-aware datetime."""
    target_tz = pytz.timezone(tz_str)
    dt = parser.isoparse(utc_dt_str)
    return dt.astimezone(target_tz)


def get_temp_at_hour(
    raw_data: list[dict], target_hour_str: str, tz_str: str
) -> List[TemperatureForecast]:
    """Get temperature at a given local hour each day, interpolate if needed."""
    series = []
    
    for entry in raw_data:
        dt_local = to_timezone(entry["time"], tz_str)
        temp = entry["data"]["instant"]["details"]["air_temperature"]
        series.append((dt_local, temp))

    series.sort()

    target_hour = datetime.strptime(target_hour_str, "%H:%M").time()
    tz = pytz.timezone(tz_str)
    daily = defaultdict(list)

    for dt, temp in series:
        daily[dt.date()].append((dt, temp))

    results = []
    for date, times in daily.items():
        target_dt = tz.localize(datetime.combine(date, target_hour))
        timestamps = [dt for dt, _ in times]
        temps = [temp for _, temp in times]

        if target_dt in timestamps:
            idx = timestamps.index(target_dt)
            results.append(
                TemperatureForecast(time=target_dt.isoformat(), temperature=temps[idx])
            )
        else:
            pos = bisect.bisect(timestamps, target_dt)
            if 0 < pos < len(timestamps):
                dt0, dt1 = timestamps[pos - 1], timestamps[pos]
                t0, t1 = temps[pos - 1], temps[pos]
                weight = (target_dt - dt0).total_seconds() / (dt1 - dt0).total_seconds()
                interp_temp = t0 + weight * (t1 - t0)
                results.append(
                    TemperatureForecast(
                        time=target_dt.isoformat(), temperature=round(interp_temp, 1)
                    )
                )
            else:
                pass
                results.append(
                    {"timestamp": target_dt.isoformat(), "temperature": None}
                )

    return results

