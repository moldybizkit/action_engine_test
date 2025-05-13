from pydantic import BaseModel

from models.location import GeoTimeZone


class TemperatureForecast(BaseModel):
    time: str
    temperature: float
    
class CityTemperatureForecast(BaseModel):
    city: str
    geo_tz: GeoTimeZone
    forecast: list[TemperatureForecast]