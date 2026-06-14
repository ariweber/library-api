from database.connection import get_connection


class MemberDB:
    def __init__(self):
        pass


    def create_member(self,data: dict):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO members (email, name) VALUES (%s, %s)"
        values =(data["email"], data["name"]) 
        cursor.execute(sql, values)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id


    def get_all_members(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def get_book_by_id(self,id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members WHERE id = %s",(id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data


    def update_book(self, id: int, data: dict):
        conn = get_connection()
        cur = conn.cursor()
        lst = [f"{key} =%s" for key in data.keys()]
        keys = ",".join(lst)
        sql = f"""UPDATE members SET {keys} WHERE id = %s"""
        values = list(data.values()) + [id]
        cur.execute(sql,values)
        chench = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return chench
        

        

    def deactivate_member(id):
        conn = get_connection()
        cur = conn.cursor()
        sql = "UPDATE members SET is_activate = 0"

    def books_total_count(self):
        pass

    def count_available_books(self):
        pass

    def count_by_genre(self, genre):  
        pass

    def count_active_borrows_by_member(self, member_id):
        pass  

a = BookDB()
data = {"title": "The Silent Island",
    "author": "Jack Howard",
    "genre": "Fiction"}
print(a.get_book_by_id(3))
print(a.update_book(3,data))
