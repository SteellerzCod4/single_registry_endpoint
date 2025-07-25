from .database import AsyncSessionLocal
from sqlalchemy.future import select
from fastapi import HTTPException, status
from schemes.user import UserSignUp
from .models import User
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(user_email: str) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == user_email)
        )

        return result.scalar_one_or_none()

async def get_user_by_login(user_login: str) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.login == user_login)
        )

        return result.scalar_one_or_none()
    
async def create_user(user_data: UserSignUp):
    user = await get_user_by_email(user_data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже зарегистрирован"
        )

    user = await get_user_by_login(user_data.login)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким login уже зарегистрирован"
        )

    async with AsyncSessionLocal() as session:
        hashed_pw = pwd_context.hash(user_data.password)

        user = User(
            login=user_data.login,
            username=user_data.username,
            hashed_password=hashed_pw,
            email=user_data.email,
            is_active=True
        )

        session.add(user) 
        await session.commit()
        await session.refresh(user)

        return user

    