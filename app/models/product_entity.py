from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary, Text, Numeric
from sqlalchemy.orm import relationship
from sympy import false

from app.models import Base


class ProductEntity(Base):
    __tablename__  = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=false)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    description = Column(Text, nullable=false)
    price = Column(Numeric(10, 2), nullable=false)
    image = Column(LargeBinary)
    created_at = Column(DateTime(timezone=False), default=datetime.now, nullable=False)

    category = relationship(
        'CategoryEntity', back_populates='products', lazy='joined'
    )
    attributes = relationship(
        'ProductAttributeEntity', back_populates='product', cascade='all, delete-orphan', lazy='selectin'
    )
    cart_item = relationship(
        'CartItemEntity', back_populates='product', lazy='noload'
    )
    order_item = relationship(
        'OrderItemEntity', back_populates='product', lazy='noload'
    )
