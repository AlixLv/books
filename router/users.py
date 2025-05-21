
from fastapi import APIRouter, Path, HTTPException, Depends, status
from datetime import timedelta
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
    print(f"🌼 type user_db: {type(user_db)}")
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
        

@router.post("/me/change_password")
async def reset_password(current_user: Annotated[User, Depends(get_current_user)], data:UserChangePassword):    
    with SessionLocal() as db:
        if not verify_password(data.old_password, current_user.password):
            raise  HTTPException(
                status_code = 400,
                detail = "L'ancien mot de passe de correspond pas.",
                headers = {"X_error_Code": "INCORRECT_DATA_IN_FORM"},
            )
            
        if data.new_password != data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le nouveau mot de passe et sa confirmation sont différentes.",
                headers = {"X_error_Code": "INCORRECT_DATA_IN_FORM"},
                )
        
        print(f"👩‍🦰 CURRENT USER BEFORE UDPATE: {current_user.name}, {current_user.password}")
            
        new_hashed_password = get_password_hash(data.new_password)
        print(f"🟣 NEW PASSWORD: {data.new_password}, NEW HASHED PASSWORD: {new_hashed_password}")
        current_user.password = new_hashed_password
        db.add(current_user)
        db.commit() 
        print(f"✅ Le password de {current_user.name} a bien été modifié: {current_user.password}")
    
    # annuler le token en cours
    # déconnecter le User pour qu'iel se connecte à nouveau et obtienne un nouveau Token 
    
            
            