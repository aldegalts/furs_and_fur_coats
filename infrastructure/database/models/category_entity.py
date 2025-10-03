from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.models import Base


class CategoryEntity(Base):
    __tablename__  = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    parent = relationship(
        'CategoryEntity', remote_side=[id], backref='subcategories', lazy='joined'
    )
    products = relationship(
        'ProductEntity', back_populates='category', lazy='selectin'
    )