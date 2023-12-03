from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer

from app.core.security import get_payload
from app.utils.external_api import get_currency_list, exchange_currency
from app.api.models import CurrencyList, ExchangeResult


currency_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@currency_router.get("/list", response_model=CurrencyList)
async def get_currencies_list(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = get_payload(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        currencies = await get_currency_list()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "currencies": currencies
    }


@currency_router.get("/exchange", response_model=ExchangeResult)
async def read_protected_data(
    base: str, target: str, amount: int, token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = get_payload(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        result = await exchange_currency(base, target, amount)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "result": result
    }
