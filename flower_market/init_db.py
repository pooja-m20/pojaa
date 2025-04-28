import sqlite3

conn = sqlite3.connect('flower_shop.db')
c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS bouquets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bouquet_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id)
)
''')


c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL
)
''')

# Create order_items table
c.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    bouquet_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id)
)
''')

# Insert sample data
c.execute('INSERT INTO bouquets (name, price, image_url) VALUES (?, ?, ?)',
          ('pink Roses ', 500, 'statics//rose.jpg'))
c.execute('INSERT INTO bouquets (name, price, image_url) VALUES (?, ?, ?)',
          ('Sunflower ', 14.99, 'statics//rose.jpg'))
c.execute('INSERT INTO bouquets (name, price, image_url) VALUES (?, ?, ?)',
          ('Tuliplyya', 17.99, 'statics//rose.jpg'))
c.execute('INSERT INTO bouquets (name, price, image_url) VALUES (?, ?, ?)',
          ('pink color', 17.99, 'statics//rose.jpg'))




conn.commit()
conn.close()
print("Database initialized successfully.")
