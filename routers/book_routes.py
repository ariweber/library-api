from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from database.book_db import BookDB
from database.connection import DBconnection


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

crud = BookDB(DBconnection())


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

@router.get("/{id}")
def get_by_id(id: int):
    book = crud.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book {id} not found")
    return book

@router.put("/{id}/borrow/{member_id}")
def borrow(id: int, member_id: int):
    changed = crud.set_available(id, "borrow", member_id)
    if not changed:
        raise HTTPException(404, f"book {id} not found")
    return {"id": id, "status": "borrowed", "member_id": member_id}

@router.put("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    changed = crud.set_available(id, "return", member_id)
    if not changed:
        raise HTTPException(404, f"book {id} not found")
    return {"id": id, "status": "returned"}


@router.get("/summary/reports")
def count_all_books():
    return {
        "total": crud.books_total_count(),
        "available": crud.count_available_books()}

