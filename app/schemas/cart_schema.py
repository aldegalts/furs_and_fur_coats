from typing import List

from pydantic import BaseModel, ConfigDict

from app.schemas.cart_item_schema import CartItemResponse


class CartBase(BaseModel):
    pass


class CartCreate(BaseModel):
    user_id: int


class CartResponse(CartBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class CartWithItemsResponse(CartResponse):
    items: List['CartItemResponse'] = []