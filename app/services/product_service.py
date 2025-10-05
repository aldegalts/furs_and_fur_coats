from typing import List

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

    def get_products(self, filters: ProductFilterRequest) -> List[ProductResponse]:
        if filters.min_price is not None and filters.max_price is not None:
            if filters.min_price > filters.max_price:
                raise IncorrectPriceInFilter()

        products = self.repository.get_filtered_products(
            category_id=filters.category_id,
            min_price=filters.min_price,
            max_price=filters.max_price,
            sort_by_price=filters.sort_by_price
        )

        if not products:
            return []

        return [ProductResponse.model_validate(product) for product in products]