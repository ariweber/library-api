import mysql.connector
from  mysql.connector import Error


class DBconnection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password= "1234"
        self.database="library_db"

    def connection(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        except Error as e:
            print(f"database error {e}")


    def create_tables(self):
        conn = self.connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(50) UNIQUE,
        name VARCHAR(50) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        borrows_total INT DEFAULT 0)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(50) UNIQUE,
        author VARCHAR(50) NOT NULL,
        genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),                  
        is_available BOOLEAN DEFAULT TRUE,
        borrowed_by_member_id INT DEFAULT 0) """)
        conn.commit()
        cursor.execute("SHOW TABLES")
        a = cursor.fetchall()
        cursor.close() 
        conn.close()
        return a






    