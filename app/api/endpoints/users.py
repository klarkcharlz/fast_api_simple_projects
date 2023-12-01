from fastapi import Depends, HTTPException, APIRouter
from fastapi import status

from app.api.database import get_session, async_session
from app.api.models import UserCreate, UserInDB, UserLogin
from app.api.services import UserCRUD
from app.core.security import create_access_token


users_router = APIRouter()
user_crud = UserCRUD()


@users_router.post("/register/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: async_session = Depends(get_session)):
    db_user = await user_crud.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = await user_crud.create(db, user)
    return new_user


@users_router.post("/login/")
async def login_for_access_token(
    user: UserLogin, db: async_session = Depends(get_session)
):
    db_user = await user_crud.get_user(db, user.username)
    if not user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
