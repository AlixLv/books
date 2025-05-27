from dataclasses import dataclass
from typing import Optional
from schemas.book_schemas import *

##### DATACLASS FOR FILTERING ##### 
@dataclass
class BookFilter:
    title: Optional[str] = None
    author: Optional[str] = None
    availability: Optional[AvailabilityEnum] = None
    category: Optional[CategoriesEnum] = None
    favourite: Optional[bool] = None 
    