from app.error.app_exception import NotFoundException, ValidationException


class CategoryNotFoundException(NotFoundException):
    def __init__(self, category_id: int):
        message = f"Категория с ID {category_id} не найдена"
        super().__init__(message, {'category_id': category_id})


class CircularCategoryReferenceException(ValidationException):
    def __init__(self, category_id: int, parent_id: int):
        message = f"Обнаружена циклическая ссылка: категория {category_id} не может быть родителем для {parent_id}"
        super().__init__(message, {
            'category_id': category_id,
            'parent_id': parent_id
        })