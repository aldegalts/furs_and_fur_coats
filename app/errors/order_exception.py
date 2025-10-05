from app.errors.app_exception import NotFoundException, ValidationException, AuthorizationException, \
    BusinessLogicException


class OrderNotFoundException(NotFoundException):
    def __init__(self, order_id: int):
        message = f"Заказ с ID {order_id} не найден"
        super().__init__(message, {'order_id': order_id})


class OrderItemNotFoundException(NotFoundException):
    def __init__(self, order_item_id: int):
        message = f"Товар с ID {order_item_id} не найден в заказе"
        super().__init__(message, {'order_item_id': order_item_id})


class EmptyOrderException(ValidationException):
    def __init__(self):
        super().__init__("Заказ должен содержать минимум один товар")


class OrderAccessDeniedException(AuthorizationException):
    def __init__(self, order_id: int, user_id: int):
        message = f"У пользователя {user_id} нет доступа к заказу {order_id}"
        super().__init__(message, {
            'order_id': order_id,
            'user_id': user_id
        })


class OrderAlreadyProcessedException(BusinessLogicException):
    def __init__(self, order_id: int):
        message = f"Заказ {order_id} уже обработан и не может быть изменен"
        super().__init__(message, {'order_id': order_id})