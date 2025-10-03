from typing import Any

from app.error.app_exception import NotFoundException, ValidationException, BusinessLogicException


class ProductNotFoundException(NotFoundException):
    def __init__(self, product_id: int):
        message = f"Продукт с ID {product_id} не найден"
        super().__init__(message, {'product_id': product_id})


class InvalidPriceException(ValidationException):
    def __init__(self, price: Any):
        message = f"Цена должна быть больше 0, получено: {price}"
        super().__init__(message, {'price': price})


class ProductWithoutAttributesException(ValidationException):
    def __init__(self, product_id: int):
        message = f"Продукт должен иметь минимум один атрибут"
        super().__init__(message, {'product_id': product_id})


class InsufficientStockException(BusinessLogicException):
    def __init__(self, product_id: int, available: int, requested: int):
        message = f"Недостаточно товара. Доступно: {available}, запрошено: {requested}"
        super().__init__(message, {
            'product_id': product_id,
            'available': available,
            'requested': requested
        })