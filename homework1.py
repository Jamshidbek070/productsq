import requests
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                price REAL
            )
        """)
        self.conn.commit()
        return self

    def save_products(self, products):
        for product in products:
            try:
                self.cursor.execute("""
                    INSERT INTO products (id, title, description, price)
                    VALUES (?, ?, ?, ?)
                """, (product['id'], product['title'], product['description'], product['price']))
            except sqlite3.Error as e:
                print(f"Xatolik: {e} -> {product}")
        self.conn.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()


response = requests.get("https://dummyjson.com/products")
if response.status_code == 200:
    products = response.json().get("products", [])
    print(products)

    with DatabaseManager("products.db") as db:
        db.save_products(products)

    print("Ma'lumotlar muvaffaqiyatli saqlandi!")
else:
    print("API bilan bog'lanishda xatolik yuz berdi!")
