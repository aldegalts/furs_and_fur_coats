from sqlalchemy.orm import Session

from infrastructure.database.models import OrderItemEntity


class OrderItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, item_id: int) -> OrderItemEntity | None:
        return (
            self.session.query(OrderItemEntity)
            .filter(OrderItemEntity.id == item_id)
            .first()
        )

    def add(self, item: OrderItemEntity) -> OrderItemEntity:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item: OrderItemEntity) -> None:
        self.session.delete(item)
        self.session.commit()
