#from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLAlechmyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


##### ENUM #####
class AvailabilityEnum(str, Enum):
    borrowed = "borrowed"
    lent = "lent"
    bought =" bought"


class StatusEnum(str, Enum):
    read = "read"
    unread = "unread"    


class CategoriesEnum(str, Enum):
    essay = "essay"
    fiction = "fiction"
    autobiography = "autobiography"
    comics = "comics"
    manga = "manga"
    graphic_novel = "graphic_novel" 
    fine_book = "fine_book"
 
 
##### SCHEMAS FOR API VALIDATION #####    
#@dataclass
class BookSchema(BaseModel):
    id: int = None
    title: str
    author: str
    availability: AvailabilityEnum
    status: StatusEnum
    category: CategoriesEnum
    favourite: bool
    
    class Config:
        use_enum_values = True
        orm_mode = True


class UserSchema(BaseModel):
    id: int = None
    name: str
    email: str
    password: str
    
    class Config:
        # configuration Pydantic pour convertir objets SQLAlchemy en schémas Pydantic
        orm_mode = True
 
 
##### MODELS FOR DATABASE ##### 
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    books = relationship("Book", back_populates="owner")


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


  