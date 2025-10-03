from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from app.schemas.order_item_schema import OrderItemResponse


class OrderBase(BaseModel):
    pass


class OrderCreate(BaseModel):
    user_id: int


class OrderResponse(OrderBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderWithItemsResponse(OrderResponse):
    items: List['OrderItemResponse'] = []