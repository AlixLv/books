from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
  
    class Config:
        # configuration Pydantic pour convertir objets SQLAlchemy en schémas Pydantic
        orm_mode = True


class UserLogged(UserSchema):
    password: str
    class Config:
        orm_mode = True    

class UserId(UserSchema):
    id: int
    class Config:
        orm_mode = True    