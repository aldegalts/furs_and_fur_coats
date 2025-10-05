from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


if TYPE_CHECKING:
    from app.schemas.product_attribute_schema import ProductAttributeResponse


class ProductFilterRequest(BaseModel):
    category_id: Optional[int] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    sort_by_price: Optional[str] = "desc"

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    name: str
    category_id: int
    description: str
    price: Decimal
    image: str
    attributes: List['ProductAttributeResponse']

    model_config = ConfigDict(from_attributes=True)
