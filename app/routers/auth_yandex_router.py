from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.services.auth_yandex_service import AuthYandexService
from infrastructure.database.database_session import get_db
from app.schemas.auth_schema import TokenPairResponse

import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth/yandex", tags=["Yandex OAuth"])

YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
YANDEX_REDIRECT_URI = os.getenv("YANDEX_REDIRECT_URI")


@router.get("/login")
def login_redirect():
    url = (
        "https://oauth.yandex.ru/authorize?"
        f"response_type=code&client_id={YANDEX_CLIENT_ID}&redirect_uri={YANDEX_REDIRECT_URI}"
    )
    return RedirectResponse(url)


@router.get("/callback", response_model=TokenPairResponse, status_code=status.HTTP_200_OK)
def callback(code: str, db: Session = Depends(get_db)):
    service = AuthYandexService(db)
    return service.login_or_register(code)
