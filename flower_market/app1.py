from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE bouquets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    image_url TEXT
);

-- cart table (simple cart for one user; for multi-user, add user_id)
CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bouquet_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id)
);

-- orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT,
    total_amount REAL
);


CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    bouquet_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id)
);

  )   
   ''')


def get_db():
    conn = sqlite3.connect('flower_shop.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    db = get_db()
    bouquets = db.execute('SELECT * FROM bouquets').fetchall()
    return render_template('index.html', bouquets=bouquets)


@app.route('/add_to_cart/<int:bouquet_id>', methods=['POST'])
def add_to_cart(bouquet_id):
    db = get_db()
    db.execute('INSERT INTO cart (bouquet_id, quantity) VALUES (?, ?)', (bouquet_id, 1))
    db.commit()
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    db = get_db()
    items = db.execute('''
        SELECT cart.id, bouquets.name, bouquets.price, bouquets.image_url, cart.quantity
        FROM cart
        JOIN bouquets ON cart.bouquet_id = bouquets.id
    ''').fetchall()
    return render_template('cart.html', items=items)


@app.route('/place_order', methods=['POST'])
def place_order():
    db = get_db()
    cart_items = db.execute('SELECT bouquet_id, quantity FROM cart').fetchall()

    total = 0
    for item in cart_items:
        price = db.execute('SELECT price FROM bouquets WHERE id=?', (item['bouquet_id'],)).fetchone()['price']
        total += price * item['quantity']

    db.execute('INSERT INTO orders (order_date, total_amount) VALUES (?, ?)',
               (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total))
    order_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

    for item in cart_items:
        db.execute('INSERT INTO order_items (order_id, bouquet_id, quantity) VALUES (?, ?, ?)',
                   (order_id, item['bouquet_id'], item['quantity']))

    db.execute('DELETE FROM cart')
    db.commit()
    return 'Order placed successfully!'


if __name__ == '__main__':
    app.run(debug=True)