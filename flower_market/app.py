from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
from datetime import datetime
import hashlib



app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.secret_key = app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flower.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey'  # for session

db = SQLAlchemy(app)

# Hash password for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize the database (if it doesn't exist)
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Sample products
PRODUCTS = [
    {'id': 1, 'name': 'Laptop', 'price': 999},
    {'id': 2, 'name': 'Headphones', 'price': 199},
    {'id': 3, 'name': 'Smartphone', 'price': 799},
]

# Initialize DB
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                product_name TEXT,
                price REAL
            )
        ''')



# Register route for new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Registered successfully. Please log in.")
            return redirect(url_for('login'))  # Corrected redirect to 'login' route
        except sqlite3.IntegrityError:
            flash("Username already exists.")
        finally:
            conn.close()

    return render_template('register.html')

# Login route for users to authenticate
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return "✅ Login successful! Welcome, " + username
        else:
            flash("Invalid credentials.")

    return render_template('login.html')

# Show signup form
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    conn = sqlite3.connect('templates/users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

    return redirect(url_for('users'))



@app.route('/index')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if product:
        cart = session.get('cart', [])
        cart.append(product)
        session['cart'] = cart
        flash(f"{product['name']} added to cart.")
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        flash(f"{removed_item['name']} removed from cart.")
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    with sqlite3.connect('database.db') as conn:
        for item in cart:
            conn.execute("INSERT INTO orders (product_id, product_name, price) VALUES (?, ?, ?)",
                         (item['id'], item['name'], item['price']))
    session['cart'] = []
    flash("Order placed successfully!")
    return redirect(url_for('index'))
















@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/wedding')
def wedding():
    return render_template('wedding.html')

@app.route('/birthday')
def birthday():
    return render_template('birthday.html')

@app.route('/aniversary')
def aniversary():
    return render_template('aniversary.html')

@app.route('/delivery_information')
def delivery_information():
    return render_template('delivery_information.html')



if __name__ == '__main__':
    init_db()
    app.run(debug=True)