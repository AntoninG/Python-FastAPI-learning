"""
User model
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.utils.database import Base


# pylint: disable=too-few-public-methods
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)

    articles = relationship("Article", back_populates="author")
