from typing import Optional

from sqlalchemy.orm import Session

from app.errors.cart_exception import EmptyCartException
from app.errors import ProductNotFoundException, CartItemNotFoundException
from app.schemas import CartResponse, CartItemWithProductResponse
from infrastructure.database.models import CartEntity, CartItemEntity
from infrastructure.database.repository import CartRepository, CartItemRepository, ProductRepository


class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.cart_item_repo = CartItemRepository(db)
        self.product_repo = ProductRepository(db)

    def get_or_create_cart(self, user_id: int) -> CartEntity:
        cart = self.cart_repo.get_by_user_id(user_id)

        if not cart:
            cart = CartEntity(user_id=user_id)
            self.cart_repo.add(cart)

        return cart

    def get_cart(self, user_id: int) -> CartResponse:
        return CartResponse.model_validate(
            self.get_or_create_cart(user_id)
        )

    def add_item_to_cart(self, user_id: int, product_id: int, quantity: int) -> CartItemWithProductResponse:
        product = self.product_repo.get_by_id(product_id)

        if not product:
            raise ProductNotFoundException(product_id=product_id)

        cart = self.get_or_create_cart(user_id)

        existing_item = self.cart_item_repo.get_by_cart_id_and_product_id(cart.id, product.id)

        if existing_item:
            existing_item.quantity += quantity
            existing_item = self.cart_item_repo.refresh(existing_item)
            return CartItemWithProductResponse.model_validate(existing_item)

        cart_item = CartItemEntity(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        cart_item = self.cart_item_repo.add(cart_item)

        return CartItemWithProductResponse.model_validate(cart_item)

    def update_cart_item(self, user_id: int, item_id: int, quantity: Optional[int]) -> CartItemWithProductResponse:
        cart = self.get_or_create_cart(user_id)

        cart_item = self.cart_item_repo.get_by_item_id_and_cart_id(item_id, cart.id)

        if not cart_item:
            raise CartItemNotFoundException(cart_item_id=item_id)

        if quantity is not None:
            cart_item.quantity = quantity

        cart_item = self.cart_item_repo.refresh(cart_item)

        return CartItemWithProductResponse.model_validate(cart_item)

    def delete_cart_item(self, user_id: int, item_id: int) -> None:
        cart = self.get_cart(user_id)

        cart_item = self.cart_item_repo.get_by_item_id_and_cart_id(item_id, cart.id)

        if not cart_item:
            raise CartItemNotFoundException(cart_item_id=item_id)

        self.cart_item_repo.delete(cart_item)

    def clear_cart(self, user_id: int) -> None:
        cart = self.get_cart(user_id)

        self.cart_item_repo.delete_by_cart_id(cart.id)


    def validate_cart_not_empty(self, user_id: int) -> None:
        cart = self.get_cart(user_id)

        if not cart.items or len(cart.items) == 0:
            raise EmptyCartException()