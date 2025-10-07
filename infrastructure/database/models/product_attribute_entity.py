from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from infrastructure.database.models import Base


class ProductAttributeEntity(Base):
    __tablename__  = 'product_attributes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)

    product = relationship(
        'ProductEntity', back_populates='attributes', lazy='joined'
    )
