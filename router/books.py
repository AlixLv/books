from fastapi import APIRouter, Path
from db.supabase import session
from models.models import BookSchema, Book, UserSchema, User
from exceptions.exceptions import BookAlreadyExists


router = APIRouter()


@router.get("/all_books", response_model=list[BookSchema])
async def get_all_books():
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
        
        
@router.get("/book/{id}")
async def get_book(id:int = Path(ge=1)):
    pass        



@router.post("/new_book", response_model=[BookSchema])
async def add_book(data:BookSchema):
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