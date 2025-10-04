from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from infrastructure.database.models import Base


class UserEntity(Base):
    __tablename__  = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=False), default=datetime.now())

    cart = relationship(
        'CartEntity', back_populates='user', uselist=False, cascade='all, delete-orphan', lazy='joined'
    )
    orders = relationship(
        'OrderEntity', back_populates='user', cascade='all, delete-orphan', lazy='select'
    )

    refresh_tokens = relationship(
        'RefreshTokenEntity', back_populates='user', cascade='all, delete-orphan', lazy='select'
    )