from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.utils.auth.dependencies import get_current_user
from app.schemas import CartResponse, CartItemWithProductResponse, CartItemBase, CartItemUpdate
from app.services.cart_service import CartService
from infrastructure.database.database_session import get_db
from infrastructure.database.models import UserEntity

router = APIRouter(prefix= "/cart", tags=["Cart"])


@router.get("",
            response_model=CartResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить корзину текущего пользователя"
            )
def get_cart(
        current_user: UserEntity = Depends(get_current_user), db: Session = Depends(get_db)):
    return CartService(db).get_or_create_cart(user_id=current_user.id)


@router.post(
    "",
    response_model=CartItemWithProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить товар в корзину"
)
def add_cart_item_to_cart(
        item_data: CartItemBase,
        current_user: UserEntity = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return CartService(db).add_item_to_cart(
        user_id=current_user.id,
        product_id=item_data.product_id,
        quantity=item_data.quantity
    )


@router.put(
    "/{item_id}",
    response_model=CartItemWithProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить количество товара в корзине"
)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: UserEntity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return CartService(db).update_cart_item(
        user_id=current_user.id,
        item_id=item_id,
        quantity=item_data.quantity
    )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить товар из корзины"
)
def delete_cart_item(
    item_id: int,
    current_user: UserEntity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    CartService(db).delete_cart_item(
        user_id=current_user.id,
        item_id=item_id
    )
    return None