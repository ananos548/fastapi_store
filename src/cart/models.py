from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base
from auth.models import User
from store.models import Product


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id))
    quantity = Column(Integer, nullable=False)
    user_id = Column(UUID, ForeignKey(User.id))
    # product = relationship('Product')
