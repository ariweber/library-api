from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from database.book_db import BookDB
from database.member_db import MemberDB
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

bookdb = BookDB(DBconnection())
memberdb= MemberDB(DBconnection())

router = APIRouter(prefix="/books")


@router.post("/", status_code=201)
def add_abook(data: Bookcreate):
   return bookdb.create_book(data.model_dump())

@router.get("/")
def get_all():
    return bookdb.get_all_books()

@router.put("/")
def update(id: int, body: Bookupdate):
    return bookdb.update_book(id, body.model_dump(exclude_unset= True))

@router.get("/")
def get_by_id(id: int):
    book = bookdb.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book {id} not found")
    return book

@router.put("/{id}/borrow/{member_id}")
def borrow(id: int, member_id: int):
    member = memberdb.get_member_by_id(member_id)
    book = bookdb.get_book_by_id(id)
   
    if member is None:
        raise HTTPException(404, f"{member_id} not found")
    elif book is None:
        raise HTTPException(404,f"{id} not foun")
   
    if not memberdb.is_activate(member_id):
        raise HTTPException(400 ,f"member {member_id} is not activate") 
    elif not bookdb.book_is_availabl(id):
        print(bookdb.book_is_availabl(id))
        raise HTTPException(400, f"book {id} is not activate") 
   
    if bookdb.count_active_borrows_by_member(member_id) > 3:
        raise HTTPException(400, f" {member_id} has 3 books")
    
    bookdb.set_available(id, "borrow", member_id)
    memberdb.increment_borrows(member_id)
    return {"id": id, "status": "borrowed", "member_id": member_id}

@router.put("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    member = memberdb.get_member_by_id(member_id)
    book = bookdb.get_book_by_id(id)
    if member is None:
        raise HTTPException(404, f"{member_id} not found")
    elif book is None:
        raise HTTPException(404,f"{id} not foun")
    if book["borrowed_by_member_id"] != member_id:
        raise HTTPException(400, f"book {id} was not borrowed by member {member_id}")
    check = bookdb.set_available(id, "return", member_id)
    if not check:
        raise HTTPException(400)
    return {"id": id, "status": "returned"}



