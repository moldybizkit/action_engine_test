
from fastapi import Depends, FastAPI, Request
from clients.weather_client import MetWeatherClient
from services.forecast_service import ForecastService
from settings import Settings


def get_settings() -> Settings:
    return Settings()


def get_weather_client(request: Request) -> MetWeatherClient:
    return request.app.state.weather_client

def get_forecast_service(
    settings: Settings = Depends(get_settings),
    weather_client: MetWeatherClient = Depends(get_weather_client),
) -> ForecastService:
    return ForecastService(settings=settings, weather_client=weather_client)