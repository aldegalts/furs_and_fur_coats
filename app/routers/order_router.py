from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.auth.dependencies import get_current_user
from app.schemas import OrderWithItemsResponse
from app.services.order_service import OrderService
from infrastructure.database.database_session import get_db
from infrastructure.database.models import UserEntity

router = APIRouter(tags=["Orders"])


@router.post(
    "/order",
    response_model=OrderWithItemsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ из корзины"
)
def create_order(
        current_user: UserEntity = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return OrderService(db).create_order_from_cart(current_user.id)


@router.get(
    "/orders",
    response_model=List[OrderWithItemsResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все заказы пользователя"
)
def get_user_orders(
        current_user: UserEntity = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return OrderService(db).get_user_orders(current_user.id)


@router.get(
    "/orders/{order_id}",
    response_model=OrderWithItemsResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить конкретный заказ"
)
def get_order(
        order_id: int,
        current_user: UserEntity = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return OrderService(db).get_order_by_id(order_id, current_user.id)