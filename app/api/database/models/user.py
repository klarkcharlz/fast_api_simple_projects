import uuid

from sqlalchemy import Column, String
from passlib.context import CryptContext

from app.api.database import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    password = Column(String)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
