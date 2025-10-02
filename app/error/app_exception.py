from typing import Optional, Any


class AppException(Exception):

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    pass


class NotFoundException(AppException):
    pass


class AlreadyExistsException(AppException):
    pass


class BusinessLogicException(AppException):
    pass


class AuthenticationException(AppException):
    pass


class AuthorizationException(AppException):
    pass


class DatabaseException(AppException):
    pass
