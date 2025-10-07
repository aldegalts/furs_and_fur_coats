from typing import List

from sqlalchemy.orm import Session
from infrastructure.database.models import ProductAttributeEntity


class ProductAttributeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, attr_id: int) -> ProductAttributeEntity | None:
        return (
            self.session.query(ProductAttributeEntity)
            .filter(ProductAttributeEntity.id == attr_id)
            .first()
        )

    def list(self) -> List[ProductAttributeEntity]:
        return self.session.query(ProductAttributeEntity).all()

    def list_by_product(self, product_id: int) -> List[ProductAttributeEntity]:
        return (
            self.session.query(ProductAttributeEntity)
            .filter(ProductAttributeEntity.product_id == product_id)
            .all()
        )

    def add(self, attr: ProductAttributeEntity) -> ProductAttributeEntity:
        self.session.add(attr)
        self.session.commit()
        self.session.refresh(attr)
        return attr

    def delete(self, attr: ProductAttributeEntity) -> None:
        self.session.delete(attr)
        self.session.commit()
