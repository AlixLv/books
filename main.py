from fastapi import FastAPI, HTTPException, Path
from models.models import Book, User, BookSchema, UserSchema
from db.supabase import ENGINE, Base, session
from exceptions.exceptions import BookAlreadyExists


app = FastAPI()    


# définition des routes
@app.post("/new_book")
def add_book(data:dict) -> BookSchema:
    try:
        db = session()
        book_schema = BookSchema(**data)
        print(f"🌼 nouveau book schéma: {book_schema}")
        
        existing_book = db.query(Book).filter(Book.title == book_schema.title).first()
        
        if existing_book:
            raise BookAlreadyExists("Le livre existe déjà dans la db!", 400)
        else:
            db.add(Book(**book_schema.model_dump()))
            db.commit()
            print(f"🔥 nouveau livre ajouté avec succcès: {book_schema}")
            return book_schema
    except TypeError as e:
        print(f"❌ Erreur dans le type de data reçue: {e}")
        raise 
    except BookAlreadyExists as e:
            print(f"❌ Erreur pendant l'ajout d'un livre: {e}")
            raise e
    finally:
        db.close()
   


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


if __name__ == "__main__":
    print("Création des tables")
    # création des tables si elles n'existent pas encore
    Base.metadata.create_all(ENGINE)    
    print("Tables créées avec succès!")  