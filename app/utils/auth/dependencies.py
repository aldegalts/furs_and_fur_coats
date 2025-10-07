import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.orm import Session

from app.utils.auth.security import decode_access_token
from app.errors.user_exception import UserUnauthorizedException, UserNotFoundException
from infrastructure.database.database_session import get_db
from infrastructure.database.models.user_entity import UserEntity
from infrastructure.database.repository.user_repository import UserRepository
from app.utils.auth.oauth2 import oauth2_scheme

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
) -> UserEntity:
    payload = decode_access_token(token, SECRET_KEY, algorithms=(ALGORITHM,))

    if not payload or "sub" not in payload:
        raise UserUnauthorizedException()

    user_id = int(payload["sub"])

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise UserNotFoundException(user_id=user_id)

    return user