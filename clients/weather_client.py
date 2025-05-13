import aiohttp
from typing import Optional, Dict

class MetWeatherClient:
    def __init__(self, base_url: str, user_agent: str = "my-weather-app/1.0"):
        self.base_url = base_url
        self.user_agent = user_agent
        self._session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        if not self._session:
            self._session = aiohttp.ClientSession(headers={
                "User-Agent": self.user_agent
            })

    async def close(self):
        if self._session:
            await self._session.close()

    async def get_forecast(self, lat: float, lon: float, altitude: Optional[int] = None) -> Dict:
        if not self._session:
            raise RuntimeError("Session not initialized. Call start() first.")

        params = {"lat": lat, "lon": lon}
        if altitude is not None:
            params["altitude"] = altitude

        async with self._session.get(self.base_url, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Forecast error {resp.status}: {text}")
            return await resp.json()

