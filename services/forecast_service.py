from loguru import logger
from clients.weather_client import MetWeatherClient
from errors.service_errors import CityNotFoundError, ClientError
from helpers.temperature_filter import (
    get_temp_at_hour,
)
from models.forecast import CityTemperatureForecast
from settings import Settings


class ForecastService:
    def __init__(self, settings: Settings, weather_client: MetWeatherClient):
        self.cities_geo_tz = settings.cities_geo_tz
        self.weather_client = weather_client

    async def get_temperature_forecast_for_city_at_hour(
        self, city: str, hour: str
    ) -> CityTemperatureForecast:
        logger.info(f"Fetching forecast for city: {city}")

        geo_tz = self.cities_geo_tz.get(city, None)
        if geo_tz is None:
            raise CityNotFoundError(city=city)

        forecast = None

        try:
            forecast = await self.weather_client.get_forecast(
                lat=geo_tz.lat, lon=geo_tz.lon
            )
        except Exception as e:
            logger.error(f"Error fetching forecast for {city}: {e}")
            raise ClientError(details=str(e))

        temps_at_hour = get_temp_at_hour(
            raw_data=forecast.get("properties", {}).get("timeseries", []),
            target_hour_str=hour,
            tz_str=geo_tz.time_zone,
        )

        return CityTemperatureForecast(city=city, geo_tz=geo_tz, forecast=temps_at_hour)
