from app.errors.app_exception import NotFoundException


class CategoryNotFoundException(NotFoundException):
    def __init__(self, category_id: int):
        message = f"Категория с ID {category_id} не найдена"
        super().__init__(message, {'category_id': category_id})
