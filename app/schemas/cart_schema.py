from typing import List, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


if TYPE_CHECKING:
    from app.schemas.cart_item_schema import CartItemResponse


class CartBase(BaseModel):
    pass


class CartCreate(BaseModel):
    user_id: int


class CartResponse(CartBase):
    id: int
    user_id: int
    items: List['CartItemResponse'] = []

    model_config = ConfigDict(from_attributes=True)
