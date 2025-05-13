from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query

from api.deps import get_forecast_service
from models.forecast import CityTemperatureForecast
from services.forecast_service import ForecastService


router = APIRouter()


@router.get("/forecast")
async def get_forecast(
    city: Annotated[Optional[str], "City name to get the forecast for"] = Query(
        "belgrade"
    ),
    hour: Annotated[Optional[str], "Hour to get the forecast for (e.g. 14:00)"] = Query(
        "14:00"
    ),
    forecast_service: ForecastService = Depends(get_forecast_service)
) -> CityTemperatureForecast:
    return await forecast_service.get_temperature_forecast_for_city_at_hour(city=city, hour=hour)
