from decimal import Decimal
from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


if TYPE_CHECKING:
    from app.schemas.product_schema import ProductResponse


class OrderItemBase(BaseModel):
    product_id: int
    unit_price: Decimal
    quantity: int


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderItemWithProductResponse(OrderItemResponse):
    product: 'ProductResponse'
