from fastapi import APIRouter
from database.book_db import BookDB
from database.connection import DBconnection


router = APIRouter(prefix="/reports")


bookdb = BookDB(DBconnection())

@router.get("/reports")
def count_all_books():
    return {
        "total": bookdb.books_total_count(),
        "available": bookdb.count_available_books()}


