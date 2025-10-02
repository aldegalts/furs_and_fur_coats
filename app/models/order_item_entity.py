
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.models import Base


class OrderItemEntity(Base):
    __tablename__  = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship(
        'OrderEntity', back_populates= 'items', lazy='select'
    )
    product = relationship(
        'ProductEntity', back_populates= 'order_item', lazy='joined'
    )