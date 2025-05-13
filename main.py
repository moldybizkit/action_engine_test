from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from api.api import api_router
from api.deps import get_settings
from clients.weather_client import MetWeatherClient
from errors.service_errors import ServiceError
from middlewares.error_handler import default_exception_handler, service_error_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    client = MetWeatherClient(base_url=settings.met_weather_api_url)
    await client.start()
    app.state.weather_client = client
    yield
    await client.close()

app = FastAPI(lifespan=lifespan)


app.add_exception_handler(ServiceError, service_error_handler)
app.add_exception_handler(Exception, default_exception_handler)


app.include_router(api_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

    # Летнее, зимнее время
    # Есть способ вычислить температуру в 14 часов, даже если она есть только в текущий день. не смотря на то что есть данные о температуре в ближайщие N часов
# https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/2-2950159/Tyskland/Berlin/Berlin
# https://api.met.no/weatherapi/documentation
# https://api.met.no/weatherapi/locationforecast/2.0/documentation#Methods
