import asyncio
from typing import Dict

from httpx import AsyncClient
from fastapi import HTTPException

from app.core.settings import API_KEY


async def get_currency_list() -> Dict[str, str]:
    url = "https://api.apilayer.com/currency_data/list"
    headers = {
        "apikey": API_KEY
    }
    async with AsyncClient() as client:
        request = await client.get(url, headers=headers)

    data = request.json()

    if "error" in data:
        raise HTTPException(
            status_code=401,
            detail=data["error"]
        )

    currencies = data.get('currencies')

    if not currencies:
        raise HTTPException(
            status_code=401,
            detail="The structure of the external API response has changed"
        )

    return currencies


async def exchange_currency(from_: str, to: str, amount: int) -> float:
    url = "https://api.apilayer.com/currency_data/convert"
    headers = {
        "apikey": API_KEY
    }
    params = {
        "from": from_,
        "to": to,
        "amount": amount
    }
    async with AsyncClient() as client:
        request = await client.get(url, headers=headers, params=params)

    data = request.json()

    if "error" in data:
        raise HTTPException(
            status_code=401,
            detail=data["error"]
        )

    result = data.get("result")

    if not result:
        raise HTTPException(
            status_code=401,
            detail="The structure of the external API response has changed"
        )

    return result


if __name__ == "__main__":
    # asyncio.run(get_currency_list())
    asyncio.run(exchange_currency("USD", "EUR", 5))
