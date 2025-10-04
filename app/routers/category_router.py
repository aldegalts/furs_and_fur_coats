from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.category_service import CategoryService
from infrastructure.database.database_session import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("")
def get_categories(db: Session = Depends(get_db)):
    return CategoryService(db).get_categories_tree()
