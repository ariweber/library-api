from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Literal, Optional
from database.book_db import BookDB

class BooksIN(BaseModel):
    title: str
    author: str
    genre: Literal['Fiction', 'Non-Fiction', 'Science', 'History', 'Other']
    is_avilable: bool = True
    orrowed_by_member_id: Optional[int] =Field(None, ge=0)

crud = BookDB()


router = APIRouter(prefix="/books") 


@router.post("/", status_code=201)
def add_abook(data: BooksIN):
   return crud.create_book(data.model_dump())

