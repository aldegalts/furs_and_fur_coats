from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class CartItemEntity(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship(
        'CartEntity', back_populates='items', lazy='select'
    )
    product = relationship(
        'ProductEntity', back_populates='cart_item', lazy='joined'
    )
