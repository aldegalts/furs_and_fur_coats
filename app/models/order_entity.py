from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models import Base


class OrderEntity(Base):
    __tablename__  = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=False), default=datetime.now)

    user = relationship(
        'UserEntity', back_populates='orders', lazy='select'
    )
    items = relationship(
        'OrderItemEntity', back_populates='order', cascade='all, delete-orphan', lazy='selectin'
    )