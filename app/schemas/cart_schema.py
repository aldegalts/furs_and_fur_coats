from typing import List, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

from app.schemas import CartItemWithProductResponse

if TYPE_CHECKING:
    from app.schemas.cart_item_schema import CartItemResponse


class CartBase(BaseModel):
    pass


class CartResponse(CartBase):
    id: int
    user_id: int
    items: List['CartItemWithProductResponse'] = []

    model_config = ConfigDict(from_attributes=True)
