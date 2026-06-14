from fastapi import FastAPI
from routers.book_routes import router as router_book
from routers.member_routes import router as router_member
from routers.report_routes import router as router_report
from database.connection import DBconnection
from database.book_db import BookDB

app = FastAPI()



app.include_router(router_book)
app.include_router(router_member)
app.include_router(router_report)


if __name__ == "__main__":
    a = BookDB(DBconnection())
    print(a.get_book_by_id(100))
    
    
  


