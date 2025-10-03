from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict

from app.error import InvalidPriceException, InvalidQuantityException
from app.schemas import ProductResponse


class OrderItemBase(BaseModel):
    product_id: int
    unit_price: Decimal
    quantity: int

    @field_validator('unit_price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise InvalidPriceException(price=v)
        return v

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise InvalidQuantityException(quantity=v, min_value=1)
        return v


class OrderItemCreate(OrderItemBase):
    order_id: int


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderItemWithProductResponse(OrderItemResponse):
    product: ProductResponse
