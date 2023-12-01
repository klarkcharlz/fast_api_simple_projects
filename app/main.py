"""
uvicorn app.main:app --reload --port 5007
alembic revision --autogenerate
alembic upgrade head
"""

from fastapi import FastAPI
from app.api.endpoints import app_router


app = FastAPI()
app.include_router(app_router)
