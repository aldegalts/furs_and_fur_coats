from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


if TYPE_CHECKING:
    from app.schemas.product_schema import ProductResponse


class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None


class CartItemResponse(CartItemBase):
    id: int
    cart_id: int

    model_config = ConfigDict(from_attributes=True)


class CartItemWithProductResponse(CartItemResponse):
    product: 'ProductResponse'
