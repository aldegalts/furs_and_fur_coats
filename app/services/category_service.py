from typing import List, Dict

from sqlalchemy.orm import Session

from infrastructure.database.models import CategoryEntity
from infrastructure.database.repository import CategoryRepository


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def get_categories_tree(self):
        categories = self.repository.get_all()
        return self._build_tree(categories)

    def _build_tree(self, categories: List[CategoryEntity], parent_id=None) -> List[Dict]:
        tree = []
        for category in categories:
            if category.parent_id == parent_id:
                tree.append({
                    "id": category.id,
                    "name": category.category,
                    "subcategories": self._build_tree(categories, category.id)
                })
        return tree
