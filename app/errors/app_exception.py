from typing import Optional, Any
from fastapi import status


class AppException(Exception):

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None, code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.details = details or {}
        self.code = code

    def to_dict(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


class ValidationException(AppException):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, details, status.HTTP_422_UNPROCESSABLE_ENTITY)


class NotFoundException(AppException):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, details, status.HTTP_404_NOT_FOUND)


class AlreadyExistsException(AppException):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, details, status.HTTP_409_CONFLICT)


class BusinessLogicException(AppException):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, details, status.HTTP_400_BAD_REQUEST)


class AuthenticationException(AppException):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, details, status.HTTP_401_UNAUTHORIZED)


class AuthorizationException(AppException):
    def __init__(self, message: str = "Доступ запрещён", details: dict | None = None):
        super().__init__(message, details, status.HTTP_403_FORBIDDEN)


class DatabaseException(AppException):
    def __init__(self, message: str = "Ошибка базы данных", details: dict | None = None):
        super().__init__(message, details, status.HTTP_500_INTERNAL_SERVER_ERROR)
