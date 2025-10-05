from typing import Optional

from app.errors.app_exception import NotFoundException, AlreadyExistsException, ValidationException, \
    AuthenticationException


class UserNotFoundException(NotFoundException):
    def __init__(self, user_id: Optional[int] = None, email: Optional[str] = None):
        details = {}
        if user_id:
            details['user_id'] = user_id
            message = f"Пользователь с ID {user_id} не найден"
        elif email:
            details['email'] = email
            message = f"Пользователь с email {email} не найден"
        else:
            message = "Пользователь не найден"
        super().__init__(message, details)


class UserAlreadyExistsException(AlreadyExistsException):
    def __init__(self, email: str):
        message = f"Пользователь с email {email} уже зарегистрирован"
        super().__init__(message, {'email': email})


class WeakPasswordException(ValidationException):
    def __init__(self, min_length: int = 8):
        message = f"Пароль должен содержать минимум {min_length} символов"
        super().__init__(message, {'min_length': min_length})


class InvalidCredentialsException(AuthenticationException):
    def __init__(self):
        super().__init__("Неверный email или пароль")


class UserUnauthorizedException(AuthenticationException):
    def __init__(self):
        message = "Пользователь не авторизован"
        super().__init__(message)