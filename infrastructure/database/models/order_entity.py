
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from infrastructure.database.models import Base


class OrderEntity(Base):
    __tablename__  = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

    user = relationship(
        'UserEntity', back_populates='orders', lazy='select'
    )
    items = relationship(
        'OrderItemEntity', back_populates='order', cascade='all, delete-orphan', lazy='selectin'
    )