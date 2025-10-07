from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from infrastructure.database.database_session import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import TokenPairResponse, RefreshRequest
from app.utils.auth.oauth2 import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user"
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(
        email=user_in.email,
        password=user_in.password
    )


@router.post(
    "/login",
    response_model=TokenPairResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user"
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService(db).login_user(
        username=form_data.username,
        password=form_data.password
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user"
)
def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return AuthService(db).get_current_user(
        token=token
    )


@router.post(
    "/refresh",
    response_model=TokenPairResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh user"
)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    return AuthService(db).refresh_tokens(
        refresh_token=payload.refresh_token
    )


@router.post(
    "/logout",
    summary="Logout user"
)
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = AuthService(db).get_current_user(token)
    return AuthService(db).logout_user(user.id)

