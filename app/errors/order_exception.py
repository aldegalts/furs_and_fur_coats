from app.errors.app_exception import NotFoundException, AuthorizationException


class OrderNotFoundException(NotFoundException):
    def __init__(self, order_id: int):
        message = f"Заказ с ID {order_id} не найден"
        super().__init__(message, {'order_id': order_id})


class OrderAccessDeniedException(AuthorizationException):
    def __init__(self, order_id: int):
        message = f"Доступ к заказу с ID {order_id} запрещен"
        super().__init__(message, {'order_id': order_id})