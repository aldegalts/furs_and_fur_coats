from sqlalchemy.orm import Session

from infrastructure.database.models import CartEntity


class CartRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> CartEntity | None:
        return (
            self.session.query(CartEntity)
            .filter(CartEntity.user_id == user_id)
            .first()
        )

    def add(self, cart: CartEntity) -> CartEntity:
        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        return cart

    def delete(self, cart: CartEntity) -> None:
        self.session.delete(cart)
        self.session.commit()
