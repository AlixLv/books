from enum import Enum
from pydantic import BaseModel


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
    status: StatusEnum
    category: CategoriesEnum
    favourite: bool
    
    class Config:
        use_enum_values = True
        orm_mode = True