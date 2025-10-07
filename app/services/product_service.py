from typing import List

from graphene import Decimal
from sqlalchemy.orm import Session

from app.errors.product_exception import ProductNotFoundException, IncorrectPriceInFilter
from app.schemas import ProductResponse
from app.schemas.product_schema import ProductFilterRequest
from infrastructure.database.repository import ProductRepository


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProductRepository(db)

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id)

        return ProductResponse.model_validate(product)

    def get_products(
            self,
            category_id: int,
            min_price: Decimal,
            max_price: Decimal,
            sort_by_price: str
    ) -> List[ProductResponse]:
        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise IncorrectPriceInFilter()

        products = self.repository.get_filtered_products(
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            sort_by_price=sort_by_price
        )

        if not products:
            return []

        return [ProductResponse.model_validate(product) for product in products]