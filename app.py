from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --------------------------
# Database setup & seed data
# --------------------------

def get_db():
    conn = sqlite3.connect('v_mart.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
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
    # Seed products (50 items for showcase)
    if not c.execute('SELECT 1 FROM Products').fetchone():
        products = [
            ('Apple', 'Fresh Red Apples', 1, 1, 1.2, 50, 10),
            ('Banana', 'Sweet Bananas', 1, 1, 0.8, 60, 15),
            ('Orange', 'Juicy Oranges', 1, 1, 1.0, 55, 12),
            ('Grapes', 'Green Grapes', 1, 1, 2.0, 40, 10),
            ('Mango', 'Ripe Mangoes', 1, 1, 2.5, 35, 10),
            ('Potato', 'Fresh Potatoes', 2, 1, 0.5, 100, 20),
            ('Tomato', 'Red Tomatoes', 2, 1, 0.7, 80, 15),
            ('Carrot', 'Organic Carrots', 2, 1, 0.9, 70, 10),
            ('Onion', 'Yellow Onions', 2, 1, 0.6, 90, 20),
            ('Broccoli', 'Fresh Broccoli', 2, 1, 1.5, 45, 10),
            # ... more vegetables & dairy
            ('Milk', 'Whole Milk', 3, 2, 1.5, 50, 15),
            ('Cheese', 'Cheddar Cheese', 3, 2, 2.5, 40, 10),
            ('Butter', 'Salted Butter', 3, 2, 1.8, 35, 10),
            ('Yogurt', 'Plain Yogurt', 3, 2, 1.2, 50, 12),
            ('Bread', 'Whole Wheat Bread', 4, 1, 1.0, 60, 15),
            ('Croissant', 'Fresh Croissant', 4, 1, 1.5, 45, 12),
            ('Muffin', 'Blueberry Muffin', 4, 1, 1.2, 50, 12),
            ('Orange Juice', 'Fresh OJ', 5, 1, 2.0, 40, 10),
            ('Cola', 'Cola Drink', 5, 1, 1.0, 80, 20),
            ('Chips', 'Potato Chips', 6, 1, 1.0, 70, 15),
            ('Popcorn', 'Butter Popcorn', 6, 1, 1.2, 60, 15),
            ('Dish Soap', 'Liquid Dish Soap', 7, 1, 1.5, 40, 10),
            ('Rice', 'Basmati Rice', 8, 1, 2.0, 100, 20),
            ('Pasta', 'Italian Pasta', 8, 1, 1.5, 90, 20),
            # Add up to 50 items as needed...
        ]
        c.executemany('''
            INSERT INTO Products (name, description, category_id, supplier_id, price, stock_quantity, min_stock_level)
            VALUES (?,?,?,?,?,?,?)
        ''', products)
    conn.commit()
    conn.close()

# --------------------------
# Routes
# --------------------------

@app.route('/')
def index():
    conn = get_db()
    products = conn.execute('''
        SELECT p.*, c.name AS category_name, s.name AS supplier_name
        FROM Products p
        JOIN Categories c ON p.category_id = c.category_id
        JOIN Suppliers s ON p.supplier_id = s.supplier_id
    ''').fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Add Product, Edit Product, Delete Product, Low Stock, Categories, Suppliers routes here...

# --------------------------
# Run
# --------------------------

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
