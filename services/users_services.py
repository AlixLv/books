import os
from dotenv import load_dotenv
from typing import Annotated
import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status, Header 
from fastapi.security import OAuth2PasswordBearer
from db.supabase import SessionLocal
from datetime import datetime, timedelta, timezone
from models.user_models import User
from schemas.user_schemas import *
from models.blacklist_token_models import BlacklistedToken


load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


# création instance de la classe OAuth2PasswordBearer, avec en paramètre tokenURL, 
# qui contient l'url que le client va utiliser pour envoyer ses data (username, password) afin d'obtenir un token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_password_hash(password):
    # hashpw() hashes une string et génère un salt hash alétoire
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
        # on stocke le hash comme string
        ).decode("utf-8")


def verify_password(plain_password, hashed_password):
    # checkpw() compare le password en string en clair avec le password hashé en db
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        # on convertit le hash stocké en bytes
        hashed_password.encode("utf-8")
        )


def get_user(username:str):
    with SessionLocal() as db:
        return db.query(User).filter(User.name == username).first()


def authenticate_user(username: str, password:str):
    user = get_user(username)  
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user 
    

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print(f"🔍 Token received: {token[:20]}...")
    
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "L'utilisateur n'est pas authentifié",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    
    if is_token_blacklisted(token):
        raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Token invalide ou expiré. Veuillez vous reconnecter",
        headers = {"WWW-Authenticate": "Bearer"},
    )
        
    try:
        algorithm = os.environ.get("ALGORITHM", "HS256")
        if not algorithm:
            algorithm="HS256"
        print(f"🔑 Using algorithm for decoding: {algorithm}")  
        
        secret_key = os.environ.get("SECRET_KEY")
        if not secret_key:
            raise ValueError("SECRET_KEY must be set in .env file")
    
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        print(f"🐹 PAYLOAD: {payload}")
        username = payload.get("sub")
        print(f"🦊 USERNAME: {username}")
        if username is None:
            print(f"🐙 EXCEPTION 1: username is None")
            raise credentials_exception
        token_data = TokenData(username=username)
        print(f"🦁 TOKEN DATA: {token_data}")
    
    except InvalidTokenError as e:  
        print(f"🐙 EXCEPTION 2: {str(e)} ")
        raise credentials_exception
    except Exception as e:
        print(f"⚠️ Unexpected error: {str(e)}")
        raise credentials_exception

    user = get_user(token_data.username)
    print(f"🐸 USER: {user.name}, {type(user)}") 
    if user is None:
        print(f"🐙 EXCEPTION 3: User not found")
        raise credentials_exception
    return user 


def create_access_token(data: dict, expires_delta: Annotated[timedelta, None]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    algorithm = os.environ.get("ALGORITHM", "HS256")
    if not algorithm:
        algorithm="HS256"
    print(f"🔑 Using algorithm: {algorithm}")    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=algorithm)
   
    return encoded_jwt        


def is_token_blacklisted(token:str):
    with SessionLocal() as db:
        blacklisted = db.query(BlacklistedToken).filter(BlacklistedToken.token == token).first()
        if blacklisted is None:
            return False
        return True


def add_blacklist_token(token:str, expires_at:datetime, user_id:UserId):
    with SessionLocal() as db:
        blacklisted_token = BlacklistedToken(token=token, expires_at=expires_at, user_id=user_id)    
        db.add(blacklisted_token)
        db.commit()


def clean_expired_token():
    with SessionLocal() as db:
        today = datetime.now()
        expired_tokens = db.query(BlacklistedToken).filter(BlacklistedToken.expires_at < today)
        for token in expired_tokens:
            db.delete(token)
        db.commit()
            
               