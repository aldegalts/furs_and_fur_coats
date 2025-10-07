from sqlalchemy.orm import Session

from app.errors.cart_exception import EmptyCartException
from app.errors.order_exception import OrderNotFoundException, OrderAccessDeniedException
from app.schemas import OrderResponse
from app.services.cart_service import CartService
from infrastructure.database.models import OrderEntity, OrderItemEntity
from infrastructure.database.repository import OrderRepository, OrderItemRepository
from app.services.email_service import EmailService


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)
        self.cart_service = CartService(db)
        self.email_service = EmailService()

    def create_order_from_cart(self, user_id: int, user_email: str) -> OrderResponse:
        cart = self.cart_service.get_or_create_cart(user_id)

        if not cart.items or len(cart.items) == 0:
            raise EmptyCartException(cart_id=cart.id)

        order = OrderEntity(user_id=user_id)
        order = self.order_repo.add(order)

        for cart_item in cart.items:
            order_item = OrderItemEntity(
                order_id=order.id,
                product_id=cart_item.product_id,
                unit_price=cart_item.product.price,
                quantity=cart_item.quantity
            )
            self.order_item_repo.add(order_item)

        self.cart_service.clear_cart(user_id)

        self.order_repo.refresh(order)

        self.email_service.send_order_confirmation(order, user_email)

        return OrderResponse.model_validate(order)

    def get_user_orders(self, user_id: int) -> list[OrderEntity]:
        return self.order_repo.get_by_user_id(user_id)

    def get_order_by_id(self, order_id: int, user_id: int) -> OrderResponse:

        order = self.order_repo.get_by_id(order_id)

        if not order:
            raise OrderNotFoundException(order_id=order_id)

        if order.user_id != user_id:
            raise OrderAccessDeniedException(order_id=order_id)

        return OrderResponse.model_validate(order)