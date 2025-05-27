from enum import Enum
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional


##### ENUM #####
class AvailabilityEnum(str, Enum):
    borrowed = "borrowed"
    lent = "lent"
    bought ="bought"


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
class BookSchema(BaseModel):
    id: int = None
    title: str
    author: str
    availability: AvailabilityEnum
    category: CategoriesEnum
    favourite: bool
    class Config:
        use_enum_values = True
        orm_mode = True


##### DATACLASS FOR FILTERING ##### 
@dataclass
class BookFilter:
    title: Optional[str] = None
    author: Optional[str] = None
    availability: Optional[AvailabilityEnum] = None
    category: Optional[CategoriesEnum] = None
    favourite: Optional[bool] = None 
