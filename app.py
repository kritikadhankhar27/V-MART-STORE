from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db():
    conn = sqlite3.connect('v_mart.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Create tables
    c.execute('CREATE TABLE IF NOT EXISTS Categories (category_id INTEGER PRIMARY KEY, name TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS Suppliers (supplier_id INTEGER PRIMARY KEY, name TEXT, contact TEXT, email TEXT, address TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY,
        name TEXT, description TEXT, category_id INTEGER, supplier_id INTEGER,
        price REAL, stock_quantity INTEGER, min_stock_level INTEGER DEFAULT 10,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id),
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
    )''')
    # Seed categories
    categories = ['Fruits','Vegetables','Dairy','Bakery','Beverages','Snacks','Household','Staples']
    for name in categories:
        c.execute('INSERT OR IGNORE INTO Categories (name) VALUES (?)', (name,))
    # Seed suppliers
    suppliers = [('Fresh Farms', '12345', 'farm@fresh.com', 'Farm Road'),
                 ('Daily Dairy', '98765', 'dairy@dairy.com', 'Dairy Lane')]
    for s in suppliers:
        c.execute('INSERT OR IGNORE INTO Suppliers (name, contact, email, address) VALUES (?,?,?,?)', s)
    # Seed products (50+ items)
    if not c.execute('SELECT 1 FROM Products').fetchone():
        products = [
            ('Apple','Fresh Red Apples',1,1,1.2,50,10),
            ('Banana','Sweet Bananas',1,1,0.8,40,10),
            ('Orange','Juicy Oranges',1,1,1.0,35,10),
            # ... add 47 more items for showcase
        ]
        c.executemany('''INSERT INTO Products (name, description, category_id, supplier_id, price, stock_quantity, min_stock_level)
                         VALUES (?,?,?,?,?,?,?)''', products)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    products = conn.execute('SELECT p.*, c.name AS category_name FROM Products p JOIN Categories c ON p.category_id=c.category_id').fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Add other CRUD routes here...

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
