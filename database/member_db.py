class MemberDB:
    def __init__(self, db):
        self.db = db

    def create_member(self, data: dict):
        conn = self.db.connection()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO members (name, email) VALUES (%s, %s)"
            values = (data["name"], data["email"])
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def get_all_members(self):
        conn = self.db.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM members")
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def get_member_by_id(self, id):
        conn = self.db.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
            return cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def update_book(self, id: int, data: dict):
        conn = self.db.connection()
        cur = conn.cursor()
        try:
            lst = [f"{key} =%s" for key in data.keys()]
            keys = ",".join(lst)
            sql = f"""UPDATE members SET {keys} WHERE id = %s"""
            values = list(data.values()) + [id]
            cur.execute(sql, values)
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def deactivate_member(self, id):
        conn = self.db.connection()
        cur = conn.cursor()
        try:
            sql = "UPDATE members SET is_active = %s WHERE id = %s"
            cur.execute(sql, (0, id))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def activate_member(self, id):
        conn = self.db.connection()
        cur = conn.cursor()
        try:
            sql = "UPDATE members SET is_active = 1 WHERE id = %s"
            cur.execute(sql, (id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def increment_borrows(self, id):
        conn = self.db.connection()
        cur = conn.cursor()
        try:
            sql = "UPDATE members SET borrows_total = borrows_total + 1 WHERE id = %s"
            cur.execute(sql, (id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()


    def is_activate(self, id):
        member = self.get_member_by_id(id)
        if member == None:
            return None
        return member["is_active"] == 1
    
    def amount_books_by_member(self,id):
        member = self.get_member_by_id(id)
        if member is None:
            return None
        return member["borrows_total"] < 3