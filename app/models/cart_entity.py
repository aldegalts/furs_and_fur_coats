from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class CartEntity(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    user = relationship(
        'UserEntity', back_populates='cart', lazy='select'
    )
    items = relationship(
        'CartItemEntity', back_populates='cart', cascade='all, delete-orphan', lazy='selectin'
    )
