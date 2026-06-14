


class BookDB:
    def __init__(self, db):
        self.conn = db.connection()

    def close(self):
        self.conn.close()

    def create_book(self, data: dict):
        cursor = self.conn.cursor()
        try:
            sql = "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)"
            values = (data["title"], data["author"], data["genre"])
            cursor.execute(sql, values)
            self.conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def get_all_books(self):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_book_by_id(self, id):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def update_book(self, id: int, data: dict):
        if not data:
            return False
        cur = self.conn.cursor()
        try:
            lst = [f"{key} = %s" for key in data.keys()]
            keys = ", ".join(lst)
            sql = f"UPDATE books SET {keys} WHERE id = %s"
            values = list(data.values()) + [id]
            cur.execute(sql, values)
            self.conn.commit()
            return cur.rowcount
        finally:
            cur.close()

    def set_available(self, id, val, member_id):
        cur = self.conn.cursor()
        try:
            sql = "UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE id = %s"
            if val == "borrow":
                cur.execute(sql, (0, member_id, id))
            elif val == "return":
                cur.execute(sql, (1, None, id))
            else:
                raise ValueError("invalid val")
            self.conn.commit()
            return cur.rowcount
        finally:
            cur.close()

    def books_total_count(self):
        cur = self.conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT COUNT(id) as total FROM books")
            return cur.fetchone()
        finally:
            cur.close()

    def count_available_books(self):
        cur = self.conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT COUNT(id) as total FROM books WHERE is_available = 1")
            return cur.fetchone()
        finally:
            cur.close()

    def count_by_genre(self, genre):
        cur = self.conn.cursor(dictionary=True)
        try:
            sql = "SELECT genre, COUNT(*) as total FROM books WHERE genre = %s GROUP BY genre"
            cur.execute(sql, (genre,))
            return cur.fetchall()
        finally:
            cur.close()

    def count_active_borrows_by_member(self, member_id):
        cur = self.conn.cursor(dictionary=True)
        try:
            sql = "SELECT COUNT(*) as total FROM books WHERE borrowed_by_member_id = %s"
            cur.execute(sql, (member_id,))
            return cur.fetchall()
        finally:
            cur.close()
