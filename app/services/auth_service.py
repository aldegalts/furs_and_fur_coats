import os
import secrets
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password, create_access_token, decode_access_token
from app.error import UserAlreadyExistsException, InvalidCredentialsException, WeakPasswordException
from app.error.user_exception import UserUnauthorizedException, UserNotFoundException
from app.schemas import UserCreate
from app.schemas.auth_schema import TokenPairResponse, RefreshRequest
from infrastructure.database.models import UserEntity, RefreshTokenEntity
from infrastructure.database.repository import UserRepository
from infrastructure.database.repository.refresh_token_repository import RefreshTokenRepository

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRES_DAYS"))


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)

    def register_user(self, user_in: UserCreate) -> UserEntity:
        existing = self.user_repo.get_by_email(user_in.email)
        if existing:
            raise UserAlreadyExistsException(user_in.email)
        if len(user_in.password) < 8:
            raise WeakPasswordException(min_length=8)

        user = UserEntity(email=user_in.email, password_hash=hash_password(user_in.password))
        return  self.user_repo.add(user)

    def login_user(self, form_data: OAuth2PasswordRequestForm = Depends()) -> TokenPairResponse:
        user = self.user_repo.get_by_email(form_data.username)
        if not user or not verify_password(form_data.password, user.password_hash):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            subject=str(user.id),
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
            expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        refresh_token_str = secrets.token_urlsafe(48)
        refresh_expires_at = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        self.refresh_repo.create(
            RefreshTokenEntity(
                user_id=user.id,
                token=refresh_token_str,
                expires_at=refresh_expires_at,
            )
        )
        return TokenPairResponse(access_token=access_token, refresh_token=refresh_token_str)

    def get_current_user(self, token: str) -> UserEntity:
        payload = decode_access_token(token, SECRET_KEY, algorithms=(ALGORITHM,))
        if not payload or "sub" not in payload:
            raise UserUnauthorizedException()
        user_id = int(payload["sub"])
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user

    def refresh_tokens(self, payload: RefreshRequest) -> TokenPairResponse:
        token = self.refresh_repo.get_by_token(payload.refresh_token)
        if not token or token.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный refresh токен")
        if token.expires_at < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh токен истёк")

        self.refresh_repo.revoke(token)

        new_refresh_str = secrets.token_urlsafe(48)
        new_refresh_expires = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        self.refresh_repo.create(
            RefreshTokenEntity(
                user_id=token.user_id,
                token=new_refresh_str,
                expires_at=new_refresh_expires,
            )
        )

        access = create_access_token(
            subject=str(token.user_id),
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
            expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        return TokenPairResponse(access_token=access, refresh_token=new_refresh_str)

    def logout_user(self, user_id: int):
        self.refresh_repo.delete_user_tokens(user_id)
        return {"success": True}