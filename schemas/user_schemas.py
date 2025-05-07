from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    class Config:
        # configuration Pydantic pour convertir objets SQLAlchemy en schémas Pydantic
        orm_mode = True