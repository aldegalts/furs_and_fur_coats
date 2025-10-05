from app.errors.app_exception import NotFoundException, BusinessLogicException


class ProductNotFoundException(NotFoundException):
    def __init__(self, product_id: int):
        message = f"Продукт с ID {product_id} не найден"
        super().__init__(message, {'product_id': product_id})


class IncorrectPriceInFilter(BusinessLogicException):
    def __init__(self):
        message = "Минимальная цена не может быть больше максимальной"
        super().__init__(message)


class InsufficientStockException(BusinessLogicException):
    def __init__(self, product_id: int, available: int, requested: int):
        message = f"Недостаточно товара. Доступно: {available}, запрошено: {requested}"
        super().__init__(message, {
            'product_id': product_id,
            'available': available,
            'requested': requested
        })