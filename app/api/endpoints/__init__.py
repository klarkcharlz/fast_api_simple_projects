from fastapi import APIRouter
from .users import users_router
from .currency import currency_router

app_router = APIRouter()
app_router.include_router(users_router, prefix='/auth')
app_router.include_router(currency_router, prefix='/currency')
