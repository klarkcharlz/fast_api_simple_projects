from sqlalchemy.future import select

from app.api.database.models import User
from app.api.models import UserCreate


class UserCRUD:
    model = User

    async def get_user(self, db, username: str):
        statement = select(self.model).where(
            self.model.username == username
        )
        results = await db.execute(statement=statement)
        res = results.scalars().first()
        return res

    async def create(self, db, user: UserCreate):
        new_user = self.model(
            username=user.username,
            password=self.model.get_password_hash(user.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
