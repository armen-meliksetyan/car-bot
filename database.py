import sqlite3


class Database:
    def __init__(self, db_name, car_data):
        self.db_name = db_name
        self.car_data = car_data
        
    def store_in_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS cars
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT,
                          year TEXT,
                          price TEXT,
                          mileage TEXT,
                          image_src TEXT,
                          product_url TEXT)''')

        # Insert car data into the table
        for car in self.car_data:
            cursor.execute('INSERT INTO cars (title, year, price, mileage, image_src, product_url) VALUES (?, ?, ?, ?, ?, ?)',
                           (car.title, car.year, car.price, car.mileage, car.image_src, car.product_url))

        conn.commit()
        conn.close()

    def clear_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM cars")
        conn.commit()
        conn.close()

    def fetch(self):
        conn = sqlite3.connect(self.db_name)
        with conn:
            cursor = conn.cursor()
            select_query = 'SELECT title, year, price, mileage, image_src, product_url FROM cars'
            cursor.execute(select_query)
            cars = cursor.fetchall()
        return cars
    
    def filter_cars(self, model, year):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        select_query = 'SELECT title, year, price, mileage, image_src, product_url FROM cars WHERE '
        conditions = []

        if model.lower() != 'any':
            conditions.append(f"title LIKE '%{model}%'")

        if year is not None and str(year).lower() != 'any':
            conditions.append(f"year = {year}")

        if conditions:
            select_query += ' AND '.join(conditions)

        cursor.execute(select_query)
        cars = cursor.fetchall()

        conn.close()

        return cars
