from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, ConfigDict


if TYPE_CHECKING:
    from app.schemas.cart_schema import CartResponse


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(UserResponse):
    cart: Optional['CartResponse'] = None