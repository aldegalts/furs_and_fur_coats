from sqlalchemy.orm import Session
from infrastructure.database.models import CategoryEntity


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, category_id: int) -> CategoryEntity | None:
        return (
            self.session.query(CategoryEntity)
            .filter(CategoryEntity.id == category_id)
            .first()
        )

    def list(self) -> list[CategoryEntity]:
        return self.session.query(CategoryEntity).all()

    def add(self, category: CategoryEntity) -> CategoryEntity:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category
