from pydantic_settings import BaseSettings, SettingsConfigDict

from models.location import GeoTimeZone


class Settings(BaseSettings, extra="allow"):
    met_weather_api_url: str = "https://api.met.no/weatherapi/locationforecast/2.0/complete"

    app_host: str = "localhost"
    app_port: int = 8000

    cities_geo_tz: dict[str, GeoTimeZone] = {
        "belgrade": GeoTimeZone(lat=44.8001, lon=20.4574, time_zone="Europe/Belgrade"),
        "paris": GeoTimeZone(lat=48.8566, lon=2.3522, time_zone="Europe/Paris"),
        "moscow": GeoTimeZone(lat=55.7558, lon=37.6173, time_zone="Europe/Moscow"),
    }

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
