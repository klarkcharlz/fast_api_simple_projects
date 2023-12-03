from typing import Dict

from pydantic import BaseModel


class CurrencyList(BaseModel):
    currencies: Dict[str, str]


class ExchangeResult(BaseModel):
    result: float
