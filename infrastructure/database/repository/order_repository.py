from typing import List
from sqlalchemy.orm import Session
from infrastructure.database.models import OrderEntity


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_id: int) -> OrderEntity | None:
        return (
            self.session.query(OrderEntity)
            .filter(OrderEntity.id == order_id)
            .first()
        )

    def list(self) -> List[OrderEntity]:
        return self.session.query(OrderEntity).all()
    
    def get_by_user_id(self, user_id: int) -> List[OrderEntity]:
        return (
            self.session.query(OrderEntity)
            .filter(OrderEntity.user_id == user_id)
            .all()
        )

    def add(self, order: OrderEntity) -> OrderEntity:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def refresh(self, order: OrderEntity) -> OrderEntity:
        self.session.commit()
        self.session.refresh(order)