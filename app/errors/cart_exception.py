from typing import Optional, Any

from app.errors.app_exception import NotFoundException, ValidationException, BusinessLogicException, \
    AlreadyExistsException


class CartNotFoundException(NotFoundException):
    def __init__(self, cart_id: Optional[int] = None, user_id: Optional[int] = None):
        details = {}
        if cart_id:
            details['cart_id'] = cart_id
            message = f"Корзина с ID {cart_id} не найдена"
        elif user_id:
            details['user_id'] = user_id
            message = f"Корзина пользователя {user_id} не найдена"
        else:
            message = "Корзина не найдена"
        super().__init__(message, details)


class CartItemNotFoundException(NotFoundException):
    def __init__(self, cart_item_id: int):
        message = f"Товар с ID {cart_item_id} не найден в корзине"
        super().__init__(message, {'cart_item_id': cart_item_id})


class EmptyCartException(BusinessLogicException):
    def __init__(self, cart_id: int):
        message = "Невозможно оформить заказ: корзина пуста"
        super().__init__(message, {'cart_id': cart_id})


class ProductAlreadyInCartException(AlreadyExistsException):
    def __init__(self, product_id: int, cart_id: int):
        message = f"Товар уже добавлен в корзину. Измените количество"
        super().__init__(message, {
            'product_id': product_id,
            'cart_id': cart_id
        })