from sqlalchemy.orm import Session
from sqlalchemy import select
from db.supabase import SessionLocal, get_session
from fastapi import Depends
from models.book_models import Book
from schemas.book_schemas import BookSchema


def query_all_books(db:Session):
    query = db.query(Book)
    result = db.execute(query).scalars()
    return result


def query_one_book(db:Session, id:int):
    query = select(Book).where(Book.id==id)
    result = db.execute(query).first()
    return result


def query_add_book(db:Session, data:BookSchema):
    existing_book = db.query(Book).filter(Book.title == data.title).first()
    return existing_book
    

    

    
    
        