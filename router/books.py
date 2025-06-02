from fastapi import APIRouter, Path, HTTPException, Depends
from sqlalchemy.orm import Session
from db.supabase import get_session
from pydantic import ValidationError
from models.book_models import Book
from schemas.book_schemas import *
from schemas.book_filter import BookFilter
from services.books_services import *
from services.users_services import *
from exceptions.exceptions import BookAlreadyExists


router = APIRouter(
    prefix="/book"
)

# current_user: Annotated[User, Depends(get_current_user)], --> à rajouter dans get_all_books quand authorisation intégrée côté front
@router.get("/all", response_model=list[BookSchema])
async def get_all_books( 
    db:Session=Depends(get_session)
    ):
    all_books = query_all_books(db)  
    
    if not all_books:
        raise HTTPException(
                status_code=404,
                detail="Aucun livre enregistré dans la db!",
                headers={"X-Error-Code": "BOOKS_NOT_FOUND"}
            )

    #créer une liste de book instances de class BookSchema. 
    res = []
    for book in all_books:
        res.append(BookSchema(**book.__dict__))
    return res



@router.get("/filter", response_model=list[BookSchema])
async def filter_books(
    current_user: Annotated[User, Depends(get_current_user)], 
    filters:BookFilter = Depends(), 
    db:Session=Depends(get_session)
    ):
    res = query_all_books(db, filters)
    
    if not res:
        raise HTTPException(
                status_code=404,
                detail=f"Aucun livre ne correspond à votre recherche.",
                headers={"X-Error-Code": "BOOK_NOT_FOUND"}
                )
       
    filtered_books = []
    for book in res:
        print(f"BOOK: {book}")
        filtered_books.append(BookSchema(**book.__dict__))
    return filtered_books

            
        
@router.get("/{id}", response_model=BookSchema)
async def get_book(
    current_user: Annotated[User, Depends(get_current_user)],
    db:Session=Depends(get_session), 
    id:int = Path(ge=1)
    ):
    result = query_one_book(db, id)
    
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
async def add_book(
    current_user: Annotated[User, Depends(get_current_user)],
    data:dict, 
    db:Session=Depends(get_session)
    ):
    try:
        book_schema = BookSchema(**data)
        print(f"🌼 nouveau book schéma: {book_schema}")
        
        existing_book = query_check_book(db, book_schema)
        
        if existing_book:
            raise BookAlreadyExists()
        else:
            db.add(Book(**book_schema.model_dump()))
            db.commit()
            print(f"🔥 nouveau livre ajouté avec succcès: {book_schema}")
            return book_schema
    except ValidationError as e:
        print(f"❌ Erreur dans le type de data reçue: {e.errors()}")
         


@router.put("/update/{id}", response_model=BookSchema)
async def update_book(
    current_user: Annotated[User, Depends(get_current_user)],
    book_update:BookSchema, 
    db:Session=Depends(get_session), 
    id:int = Path(ge=1)
    ):
    result = query_one_book(db, id)
    
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Le livre id {id} n'existe pas dans la db!",
            headers={"X-Error-Code": "BOOK_NOT_FOUND"}
            )
    
    book = result[0]
    for field, value in book_update.model_dump().items():
        setattr(book, field, value)
    print(f"📙 {book.__dict__}")  
    
    db.commit()
    db.refresh(book)
    
    res = BookSchema(**book.__dict__)
    return res  
  


@router.delete("/delete/{id}", response_model=BookSchema)
async def delete_book(
    current_user: Annotated[User, Depends(get_current_user)],
    db:Session=Depends(get_session), 
    id: int = Path(ge=1)
    ):
    result = query_one_book(db, id)
    
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
