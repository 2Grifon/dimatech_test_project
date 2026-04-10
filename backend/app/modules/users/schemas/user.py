from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.modules.users.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    """Все поля для PATCH опциональны"""

    email: EmailStr | None = None
    full_name: str | None = None
    role: UserRole | None = None
    password: str | None = None
