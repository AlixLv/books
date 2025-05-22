from db.supabase import Base 
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLAlechmyEnum
from schemas.book_schemas import AvailabilityEnum, StatusEnum, CategoriesEnum, BookSchema
from models.user_models import User
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  
    title = Column(String, index=True)
    author = Column(String, index=True)
    availability = Column(SQLAlechmyEnum(AvailabilityEnum), nullable=False)
    status = Column(SQLAlechmyEnum(StatusEnum), nullable=False)
    category = Column(SQLAlechmyEnum(CategoriesEnum), nullable=False)
    favourite = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey(User.id))
    owner = relationship("User", back_populates="books")
