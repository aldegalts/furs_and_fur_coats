from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def create_access_token(*, subject: str, secret_key: str, algorithm: str = "HS256", expires_minutes: int = 60) -> str:
    now = datetime.now(timezone.utc)
    to_encode = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str, secret_key: str, algorithms: list[str] | tuple[str, ...] = ("HS256",)) -> Optional[dict]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=list(algorithms))
        return payload
    except JWTError:
        return None
