from connection import get_connection


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
        conn.close()
        return new_id


    def get_all_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def get_book_by_id(self,id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data


    def update_book(self, id: int, data: dict):
        if not data:
            return False
        conn = get_connection()
        cur = conn.cursor()
        lst = [f"{key} =%s" for key in data.keys()]
        keys = ",".join(lst)
        sql = f"""UPDATE books SET {keys} WHERE id = %s"""
        values = list(data.values()) + [id]
        cur.execute(sql,values)
        chench = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return chench
        

        

    def set_available(self, id, val, member_id):
        conn = get_connection()
        cur = conn.cursor()
        if val == "borrow":
            sql = "UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE id = %s"
            cur.execute(sql,(0,member_id,id))
        elif val == "return":
              sql = "UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE id = %s"
              cur.execute(sql,(1,None,id))
        else:
            raise ("invalid val")
        conn.commit()
        check = cur.rowcount
        cur.close()
        conn.close
        return check
              

        

       

        

        pass

    def books_total_count(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT COUNT(id) as total FROM books")
        count = cur.fetchone()
        conn.close()
        cur.close
        return count



    def count_available_books(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT COUNT(id) as total FROM books WHERE is_available = 1")
        count = cur.fetchone()
        conn.close()
        cur.close
        return count
                
        

    def count_by_genre(self, genre):
        conn = get_connection()
        cur = conn.cursor(dictionary=True) 
        sql = "SELECT genre, COUNT(*) as total FROM books WHERE genre = %s GROUP BY genre"
        cur.execute(sql,(genre,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
        

    def count_active_borrows_by_member(self, member_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True) 
        sql ="SELECT COUNT(*) as total FROM books WHERE borrowed_by_member_id = %s"
        cur.execute(sql,(member_id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
        

a = BookDB()
# print(a.set_available(2, "borrow", 30))
# print(a.get_book_by_id(2))
print(a.count_active_borrows_by_member(30))
