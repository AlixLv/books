from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.supabase import Base 
from schemas.user_schemas import UserSchema


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    books = relationship("Book", back_populates="owner")