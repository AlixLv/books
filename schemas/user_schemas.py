from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
  
    class Config:
        # configuration Pydantic pour convertir objets SQLAlchemy en schémas Pydantic
        orm_mode = True


class UserLogged(UserSchema):
    password: str  

class UserId(UserSchema):
    id: int
    class Config:
        orm_mode = True    

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    username: str | None = None           