from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from infrastructure.database.models import RefreshTokenEntity


class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, token: RefreshTokenEntity) -> RefreshTokenEntity:
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token

    def get_by_token(self, token_str: str) -> Optional[RefreshTokenEntity]:
        return (
            self.session.query(RefreshTokenEntity)
            .filter(RefreshTokenEntity.token == token_str)
            .first()
        )

    def revoke(self, token: RefreshTokenEntity) -> None:
        token.revoked = True
        self.session.add(token)
        self.session.commit()

    def delete_user_tokens(self, user_id: int) -> None:
        (
            self.session.query(RefreshTokenEntity)
            .filter(RefreshTokenEntity.user_id == user_id)
            .delete(synchronize_session=False)
        )
        self.session.commit()

    def purge_expired(self) -> int:
        count = (
            self.session.query(RefreshTokenEntity)
            .filter(RefreshTokenEntity.expires_at < datetime.now())
            .delete(synchronize_session=False)
        )
        self.session.commit()
        return count
