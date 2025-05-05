from fastapi import APIRouter, Path, HTTPException
from db.supabase import SessionLocal
from sqlalchemy import select
from pydantic import ValidationError
#from models.models import BookSchema, Book, UserSchema, User
from models.book_models import Book
from schemas.book_schemas import BookSchema
from exceptions.exceptions import BookAlreadyExists


router = APIRouter(
    prefix="/book"
)


@router.get("/all", response_model=list[BookSchema])
async def get_all_books():
    with SessionLocal() as db:
        query = db.query(Book)
        all_books = db.execute(query).scalars()
        
        if not all_books:
            raise HTTPException(
                    status_code=404,
                    detail="Aucun livre enregistré dans la db!",
                    headers={"X-Error-Code": "BOOKS_NOT_FOUND"}
                )

        # créer une liste de book instances de class BookSchema. 
        res = []
        for book in all_books:
            res.append(BookSchema(**book.__dict__))
        return res

        
        
@router.get("/{id}", response_model=BookSchema)
async def get_book(id:int = Path(ge=1)):
    with SessionLocal() as db:
        query = select(Book).where(Book.id==id)
        result = db.execute(query).first()
        
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"Le livre id {id} n'existe pas dans la base de données",
                    headers={"X-Error-Code": "BOOK_NOT_FOUND"}
                    )
        
        book = result[0]
        res = BookSchema(**book.__dict__)
        print(f"📘 {res}, {type(res)}")
        return res



@router.post("/add", response_model=BookSchema)
async def add_book(data:dict):
    try:
        with SessionLocal() as db:
            book_schema = BookSchema(**data)
            print(f"🌼 nouveau book schéma: {book_schema}")
            
            existing_book = db.query(Book).filter(Book.title == book_schema.title).first()
            
            if existing_book:
                raise BookAlreadyExists()
            else:
                db.add(Book(**book_schema.model_dump()))
                db.commit()
                print(f"🔥 nouveau livre ajouté avec succcès: {book_schema}")
                return book_schema
    except ValidationError as e:
        print(f"❌ Erreur dans le type de data reçue: {e.errors()}")
        raise 



@router.put("/update/{id}", response_model=BookSchema)
async def update_book(book_update:BookSchema, id:int = Path(ge=1)):
    with SessionLocal() as db:
        query = select(Book).where(Book.id == id)
        result = db.execute(query).first()
        
        book = result[0]
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Le livre id {id} n'existe pas dans la db!",
                headers={"X-Error-Code": "BOOK_NOT_FOUND"}
                )
        
        for field, value in book_update.model_dump().items():
            setattr(book, field, value)
        print(f"📙 {book.__dict__}")  
        
        db.commit()
        db.refresh(book)
        
        res = BookSchema(**book.__dict__)
        return res  
  


@router.delete("/delete/{id}", response_model=BookSchema)
async def delete_book(id: int = Path(ge=1)):
    with SessionLocal() as db:
        query = select(Book).where(Book.id==id)
        result = db.execute(query).first()
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"Le livre id {id} n'existe pas dans la base de données",
                headers={"X-Error-Code": "BOOK_NOT_FOUND"}
                )
        
        book = result[0]
        res = BookSchema(**book.__dict__)
        print(f"📘 {res}, {type(res)}")
        
        db.delete(book)
        db.commit()
        return res
