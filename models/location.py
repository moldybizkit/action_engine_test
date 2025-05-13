from pydantic import BaseModel


class GeoTimeZone(BaseModel):
    lat: float
    lon: float
    time_zone: str