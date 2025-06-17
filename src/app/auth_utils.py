from typing import Optional
from fastapi import Request, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models
from .database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a hash."""
    return pwd_context.verify(password, hashed)


async def get_current_user(
    request: Request, db: AsyncSession = Depends(get_db)
) -> Optional[models.User]:
    """Retrieve the currently authenticated user from the session."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalar_one_or_none()
