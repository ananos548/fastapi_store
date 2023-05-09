from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey

from database import Base


class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    published_at = Column(TIMESTAMP, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('category.category_id'))
