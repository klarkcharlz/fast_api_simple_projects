from jose import jwt

from app.core.settings import SECRET_KEY, ALGORITHM


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_payload(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

