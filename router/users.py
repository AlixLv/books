import os
from dotenv import load_dotenv
from fastapi import APIRouter, Path, HTTPException, Depends, status
from db.supabase import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from models.user_models import User
from schemas.user_schemas import UserSchema
from typing import Annotated
from datetime import datetime, timedelta
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# création instance de la classe OAuth2PasswordBearer, avec en paramètre tokenURL, qui contient l'url que le client va utiliser pour envoyer ses data (username, password) afin d'obtenir un token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    prefix="/user"
)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register", response_model=UserSchema)
async def register_user(user: dict):
    with SessionLocal() as db:
        user_schema = UserSchema(**user)
        db_user = db.query(User).filter(User.email == user_schema.email).first()
        print(f"👩‍🦰 db user: {db_user}, {type(db_user)}")
        if db_user:
            raise HTTPException(
                    status_code=404,
                    detail=f"L'email existe déjà dans la db",
                    headers={"X-Error-Code": "EMAIL_ALREADY_REGISTERED"}
            )
        
        hashed_password = get_password_hash(user_schema.password)
        db_user = User(name=user_schema.name, email=user_schema.email, password=hashed_password)
        db.add(db_user)
        db.commit()
        print(f"👑 user newly registered to db: {db_user.name}, {type(db_user)}")
        return user_schema
        