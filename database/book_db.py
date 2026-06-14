from database.connection import get_connection


class BookDB:
    def __init__(self):
        pass

    def create_book(self,data: dict):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)"
        values =(data["title"], data["author"], data["genre"]) 
        cursor.execute(sql, values)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close
        return new_id


    def get_all_books(self):
        pass

    def get_book_by_id(self,id):
        pass

    def update_book(self, id, data):
        pass

    def set_available(self, id, val, member_id):
        pass

    def books_total_count(self):
        pass

    def count_available_books(self):
        pass

    def count_by_genre(self, genre):  
        pass

    def count_active_borrows_by_member(self, member_id):
        pass  