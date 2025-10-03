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

    def list(self) -> list[ProductEntity]:
        return self.session.query(ProductEntity).all()

    def filter_by_price(self, min_price: float, max_price: float) -> list[ProductEntity]:
        return (
            self.session.query(ProductEntity)
            .filter(ProductEntity.price >= min_price, ProductEntity.price <= max_price)
            .all()
        )

    def get_by_category(self, category_id: int) -> list[ProductEntity]:
        return (
            self.session.query(ProductEntity)
            .filter(ProductEntity.category_id == category_id)
            .all()
        )

    def add(self, product: ProductEntity) -> ProductEntity:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: ProductEntity) -> None:
        self.session.delete(product)
        self.session.commit()
