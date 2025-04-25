from fastapi import FastAPI, HTTPException, Path
import json
from models.models import Base, Book, User, BookSchema, UserSchema
from db.supabase import create_supabase_client
from db.supabase import ENGINE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select 


app = FastAPI()    
supabase = create_supabase_client()

# création des tables si elles n'existent pas encore
Base.metadata.create_all(ENGINE)  

session = sessionmaker(ENGINE)



# définition des routes
@app.post("/new_book")
def add_book(data:dict) -> BookSchema:
    try:
        db = session()
        book_schema = BookSchema(**data)
        print(f"🌼 nouveau book schéma: {book_schema}")
        
        db.add(Book(**book_schema.model_dump()))
        db.commit()
        print(f"🔥 nouveau livre ajouté avec succcès: {book_schema}")
    except:
        pass
    finally:
        db.close()
    return book_schema


@app.get("/all_books")
def get_all_books()-> list[BookSchema]:
    try:
        db = session()
        res = []
        query = db.query(Book)
        all_books = db.execute(query).scalars()

        
        # créer une liste de book instances de class BookSchema. 
        for book in all_books:
            res.append(BookSchema(**book.__dict__))
 
        return res
    except:
        pass
    finally:
        db.close()


@app.get("/book/{id}")
def get_book(id:int = Path(ge=1)):
    pass

    