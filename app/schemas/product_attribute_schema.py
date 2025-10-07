from pydantic import BaseModel, ConfigDict


class ProductAttributeBase(BaseModel):
    name: str
    value: str


class ProductAttributeResponse(ProductAttributeBase):
    id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)
