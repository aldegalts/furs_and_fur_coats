from sqlalchemy.orm import Session

from infrastructure.database.models import CartItemEntity


class CartItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, item_id: int) -> CartItemEntity | None:
        return (
            self.session.query(CartItemEntity)
            .filter(CartItemEntity.id == item_id)
            .first()
        )

    def add(self, item: CartItemEntity) -> CartItemEntity:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item: CartItemEntity) -> None:
        self.session.delete(item)
        self.session.commit()
