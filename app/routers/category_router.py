from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services.category_service import CategoryService
from infrastructure.database.database_session import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get categories with subcategories"
)
def get_categories(db: Session = Depends(get_db)):
    return CategoryService(db).get_categories_tree()
