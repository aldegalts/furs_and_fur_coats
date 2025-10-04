from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.models import Base


class RefreshTokenEntity(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=False), default=datetime.now())
    expires_at = Column(DateTime(timezone=False), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)

    user = relationship('UserEntity', back_populates='refresh_tokens', lazy='joined')




