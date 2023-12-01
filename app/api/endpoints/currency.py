from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer

from app.core.security import get_payload
from app.utils.external_api import get_currency_list
from app.api.models import CurrencyList


currency_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@currency_router.get("/list", response_model=CurrencyList)
async def read_protected_data(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = get_payload(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        currencies = await get_currency_list()
        if not currencies:
            raise HTTPException(
                status_code=404,
                detail="The structure of the external API response has changed"
            )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "currencies": currencies
    }
