from fastapi import FastAPI
from routers.book_routes import router as router_book
from routers.report_routes  import router as router_member
from routers.member_routes import router as router_report
from database.connection import get_connection
from database.connection import create_tables
app = FastAPI()

app.include_router(router_book)
app.include_router(router_member)
app.include_router(router_report)


if __name__ == "__main__":
    pass
  


