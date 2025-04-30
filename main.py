from fastapi import FastAPI, HTTPException, Path
from models.models import Book, User, BookSchema, UserSchema
from db.supabase import ENGINE, Base, SessionLocal
from router import books, users
from exceptions.exceptions import BookAlreadyExists


app = FastAPI()    

app.include_router(books.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenue!"}




if __name__ == "__main__":
    print("Création des tables")
    # création des tables si elles n'existent pas encore
    Base.metadata.create_all(ENGINE)    
    print("Tables créées avec succès!")  