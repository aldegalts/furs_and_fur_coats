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

    def get_by_cart_id_and_product_id(self, cart_id: int, product_id: int) -> CartItemEntity | None:
        return (
            self.session.query(CartItemEntity)
            .filter(CartItemEntity.cart_id == cart_id, CartItemEntity.product_id == product_id)
            .first()
        )

    def get_by_item_id_and_cart_id(self, item_id: int, cart_id: int) -> CartItemEntity | None:
        return (self.session.query(CartItemEntity)
                .filter(CartItemEntity.id == item_id, CartItemEntity.cart_id == cart_id)
                .first())

    def refresh(self, item: CartItemEntity) -> CartItemEntity:
        self.session.commit()
        self.session.refresh(item)
        return item

    def add(self, item: CartItemEntity) -> CartItemEntity:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item: CartItemEntity) -> None:
        self.session.delete(item)
        self.session.commit()

    def delete_by_cart_id(self, cart_id: int) -> None:
        (self.session.query(CartItemEntity)
         .filter(CartItemEntity.cart_id == cart_id)
         .delete())
        self.session.commit()
