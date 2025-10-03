from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductAttributeBase(BaseModel):
    name: str
    value: str


class ProductAttributeCreate(ProductAttributeBase):
    product_id: int


class ProductAttributeUpdate(ProductAttributeBase):
    name: Optional[str] = None
    value: Optional[str] = None


class ProductAttributeResponse(ProductAttributeBase):
    id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)