from datetime import datetime
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, field_validator, ConfigDict
from app.error.product_exception import InvalidPriceException


if TYPE_CHECKING:
    from app.schemas.category_schema import CategoryResponse
    from app.schemas.product_attribute_schema import ProductAttributeResponse


class ProductBase(BaseModel):
    name: str
    category_id: int
    description: Optional[str] = None
    price: Decimal
    image: Optional[bytes] = None

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise InvalidPriceException(price=v)
        return v


class ProductCreate(ProductBase):
    created_at: datetime


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    image: Optional[bytes] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductDetailResponse(ProductResponse):
    category: CategoryResponse
    attributes: List['ProductAttributeResponse'] = []