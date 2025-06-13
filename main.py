from typing import Annotated
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from models.user_models import User
from models.book_models import Book
from models.blacklist_token_models import BlacklistedToken
from schemas.user_schemas import UserSchema
from db.supabase import ENGINE, Base, SessionLocal
from router import books, users
from exceptions.exceptions import ApiException
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()    

app.include_router(books.router)
app.include_router(users.router)


origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
                   )


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.headers.get("X-Error-Code") if exc.headers else None,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(ApiException)
async def book_already_exists_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.headers.get("X-Error-Code") if exc.headers else None,
            "timestamp": datetime.now().isoformat()
        }
    )  

@app.get("/")
def read_root():
    return {"message": "Bienvenue!"}


if __name__ == "__main__":
    print("Création des tables")
    # création des tables si elles n'existent pas encore
    Base.metadata.create_all(ENGINE)    
    print("Tables créées avec succès!")  