from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from infrastructure.database.database_session import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import TokenPairResponse, RefreshRequest
from app.auth.oauth2 import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(user_in)


@router.post("/login", response_model=TokenPairResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService(db).login_user(form_data)


@router.get("/me", response_model=UserResponse)
def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return AuthService(db).get_current_user(token)


@router.post("/refresh", response_model=TokenPairResponse)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    return AuthService(db).refresh_tokens(payload)


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = AuthService(db).get_current_user(token)
    return AuthService(db).logout_user(user.id)

