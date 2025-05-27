from sqlalchemy.orm import Session
from sqlalchemy import select
from db.supabase import SessionLocal, get_session
from fastapi import Depends, Form
from typing import Annotated
from models.book_models import Book
from schemas.book_schemas import *



def query_all_books(db:Session, filters:BookFilter=None):
    query = db.query(Book)
    if filters is not None:
        if filters.title is not None:
            query = query.filter(Book.title.ilike(f'%{filters.title}%'))
        if filters.author is not None:
            query = query.filter(Book.author.ilike(f'%{filters.author}%'))
        if filters.availability is not None:
            query = query.filter(Book.availability == filters.availability)
        if filters.category is not None:
            query = query.filter(Book.category == filters.category)
        if filters.favourite is not None:
            query = query.filter(Book.favourite == filters.favourite)            
    result = db.execute(query).scalars()        
    return result


def query_one_book(db:Session, id:int):
    query = select(Book).where(Book.id==id)
    result = db.execute(query).first()
    return result


def query_add_book(db:Session, data:BookSchema):
    existing_book = db.query(Book).filter(Book.title == data.title).first()
    return existing_book
    



    
    
        