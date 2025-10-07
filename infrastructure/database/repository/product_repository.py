from decimal import Decimal
from typing import List, Optional

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from infrastructure.database.models import ProductEntity


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: int) -> ProductEntity | None:
        return (
            self.session.query(ProductEntity)
            .filter(ProductEntity.id == product_id)
            .first()
        )

    def list(self) -> List[ProductEntity]:
        return self.session.query(ProductEntity).all()

    def get_filtered_products(
            self,
            category_id: Optional[int] = None,
            min_price: Optional[Decimal] = None,
            max_price: Optional[Decimal] = None,
            sort_by_price: Optional[str] = None
    ) -> List[ProductEntity]:

        query = self.session.query(ProductEntity)

        if category_id is not None:
            query = query.filter(ProductEntity.category_id == category_id)

        if min_price is not None:
            query = query.filter(ProductEntity.price >= min_price)

        if max_price is not None:
            query = query.filter(ProductEntity.price <= max_price)

        if sort_by_price == "asc":
            query = query.order_by(asc(ProductEntity.price))
        elif sort_by_price == "desc":
            query = query.order_by(desc(ProductEntity.price))

        return query.all()
