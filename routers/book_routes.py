from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal, Optional
from database.book_db import BookDB

class Bookcreate(BaseModel):
    title: str
    author: str
    genre: Literal['Fiction', 'Non-Fiction', 'Science', 'History', 'Other']
    is_avilable: bool = True
    borrowed_by_member_id: Optional[int] | None= None

class Bookupdate(BaseModel):
    title: str | None =  None
    author: str | None = None
    genre: Literal['Fiction', 'Non-Fiction', 'Science', 'History', 'Other'] | None = None
    is_avilable: bool | None = None
    borrowed_by_member_id: Optional[int] | None = None


crud = BookDB()


router = APIRouter(prefix="/books") 
    

@router.post("/", status_code=201)
def add_abook(data: Bookcreate):
   return crud.create_book(data.model_dump())

@router.get("/")
def get_all():
    return crud.get_all_books()

@router.put("/")
def update(id: int, body: Bookupdate):
    return crud.update_book(id, body.model_dump(exclude_unset= True))



