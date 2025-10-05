from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, field_validator, ConfigDict
from app.errors.cart_exception import InvalidQuantityException


if TYPE_CHECKING:
    from app.schemas.product_schema import ProductResponse


class CartItemBase(BaseModel):
    product_id: int
    quantity: int

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise InvalidQuantityException(quantity=v, min_value=1)
        return v


class CartItemCreate(CartItemBase):
    cart_id: int


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v is not None and v <= 0:
            raise InvalidQuantityException(quantity=v, min_value=1)
        return v


class CartItemResponse(CartItemBase):
    id: int
    cart_id: int

    model_config = ConfigDict(from_attributes=True)


class CartItemWithProductResponse(CartItemResponse):
    product: 'ProductResponse'
