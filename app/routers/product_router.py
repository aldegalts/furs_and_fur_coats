from typing import List

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.schemas import ProductResponse, ProductFilterRequest
from app.services.product_service import ProductService
from infrastructure.database.database_session import get_db

router = APIRouter(tags=["Product"])

@router.get("/product/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService(db).get_product_by_id(
        product_id=product_id
    )

@router.post("/products", response_model=List[ProductResponse])
def get_products(filters: ProductFilterRequest = Body(...), db: Session = Depends(get_db)):
    return ProductService(db).get_products(
        category_id=filters.category_id,
        min_price=filters.min_price,
        max_price=filters.max_price,
        sort_by_price=filters.sort_by_price
    )