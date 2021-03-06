"""
Article model
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.utils.database import Base


# pylint: disable=too-few-public-methods
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String)
    content = Column(String)

    author = relationship("User", back_populates="articles")
