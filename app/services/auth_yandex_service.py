import os
import secrets
from datetime import datetime, timedelta

import httpx
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.utils.auth.security import hash_password, create_access_token
from app.schemas.auth_schema import AccessTokenResponse, TokenPairResponse
from infrastructure.database.models import UserEntity, RefreshTokenEntity
from infrastructure.database.repository import UserRepository, RefreshTokenRepository

load_dotenv()

YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
YANDEX_CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")
YANDEX_REDIRECT_URI = os.getenv("YANDEX_REDIRECT_URI")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRES_DAYS"))

class AuthYandexService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)

    def exchange_code_for_token(self, code: str) -> AccessTokenResponse:
        token_url = "https://oauth.yandex.ru/token"
        with httpx.Client() as client:
            response = client.post(
                token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": YANDEX_CLIENT_ID,
                    "client_secret": YANDEX_CLIENT_SECRET,
                },
            )
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Ошибка обмена кода на токен Яндекса")

            return AccessTokenResponse(access_token=response.json()["access_token"])

    def get_user_info(self, access_token: AccessTokenResponse) -> dict:
        with httpx.Client() as client:
            response = client.get(
                "https://login.yandex.ru/info",
                headers={"Authorization": f"OAuth {access_token.access_token}"},
            )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Ошибка получения данных пользователя")
        return response.json()

    def login_or_register(self, code: str) -> TokenPairResponse:
        access_token_yandex = self.exchange_code_for_token(code)
        user_info = self.get_user_info(access_token_yandex)

        email = user_info.get("default_email")
        if not email:
            raise HTTPException(status_code=400, detail="Не удалось получить email от Яндекса")

        user = self.user_repo.get_by_email(email)
        if not user:
            random_password = secrets.token_urlsafe(10)
            password_hash = hash_password(random_password)
            user = UserEntity(email=email, password_hash=password_hash)
            self.user_repo.add(user)

        access_token = create_access_token(
            subject=str(user.id),
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
            expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        refresh_token_str = secrets.token_urlsafe(48)
        refresh_expires = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        self.refresh_repo.create(
            RefreshTokenEntity(
                user_id=user.id,
                token=refresh_token_str,
                expires_at=refresh_expires,
            )
        )

        return TokenPairResponse(access_token=access_token, refresh_token=refresh_token_str)