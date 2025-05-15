
from fastapi import APIRouter, Path, HTTPException, Depends, status
from datetime import datetime, timedelta, timezone
from db.supabase import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm 
from models.user_models import User
from schemas.user_schemas import *
from typing import Annotated
from services.users_services import *


router = APIRouter(
    prefix="/user"
)

# endpoint d'inscription
@router.post("/register", response_model=UserSchema)
async def register_user(user: UserLogged):
    with SessionLocal() as db:
        user_db = get_user(username=user.name)
        if user_db:
            raise HTTPException(
                    status_code=404,
                    detail=f"Le user existe déjà dans la db",
                    headers={"X-Error-Code": "EMAIL_ALREADY_REGISTERED"}
            )
        
        hashed_password = get_password_hash(user.password)
        new_db_user = User(name=user.name, email=user.email, password=hashed_password)
        db.add(new_db_user)
        db.commit()
        print(f"👑 user newly registered to db: {new_db_user.name}, {type(new_db_user)}")
        
        user_schema = UserSchema(name=new_db_user.name, email=new_db_user.email)
        return user_schema


# endpoint de connexion
@router.post("/token", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_db = authenticate_user(form_data.username, form_data.password)
    print(f"🌼 user db: {user_db.name}")
    if not user_db:
        raise HTTPException(
            status_code=400,
            detail="Nom d'utilisateur.ice ou mot de passe incorrect.",
            headers={"X_error_Code": "INCORRECT_DATA_IN_FORM"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub": user_db.name}, expires_delta=access_token_expires)    
    print(f"🪙 acces token: {access_token}")    
    user_schema = UserSchema(name=user_db.name, email=user_db.email)

    return Token(access_token=access_token, token_type="bearer")
        
        
# test endpoint protégé
@router.get("/me", response_model=UserSchema) 
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        print(f"🟠 CURRENT USER: {current_user.name}, {type(current_user)}") 
        return UserSchema(name=current_user.name, email=current_user.email)   
    except Exception as e:
        print(f"Erreur lors de la récupération du user: {e}")  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du user: {str(e)}"
        )
        
  

            
            