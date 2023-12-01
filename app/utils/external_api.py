import asyncio
from typing import Dict

from httpx import AsyncClient

from app.core.settings import API_KEY


async def get_currency_list() -> Dict[str, str]:
    url = "https://api.apilayer.com/currency_data/list"
    headers = {
        "apikey": API_KEY
    }
    async with AsyncClient() as client:
        request = await client.get(url, headers=headers)

    data = request.json()
    currencies = data.get('currencies')

    return currencies


if __name__ == "__main__":
    asyncio.run(get_currency_list())
