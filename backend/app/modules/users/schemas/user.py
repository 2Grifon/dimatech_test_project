from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

from app.modules.users.models import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
