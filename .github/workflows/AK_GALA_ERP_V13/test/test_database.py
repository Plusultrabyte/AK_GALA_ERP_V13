import sqlite3
import os

# 1. Железобетонный путь: работает из любой папки
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "store_database.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Таблицы ядра
    cur.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL,
        purchase_price REAL DEFAULT 0, selling_price REAL DEFAULT 0, stock INTEGER DEFAULT 0, min_stock INTEGER DEFAULT 0
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT, customer_phone TEXT, status TEXT DEFAULT 'active',
        total_amount REAL DEFAULT 0.0, sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, product_id INTEGER,
        product_name TEXT, quantity INTEGER, price REAL, FOREIGN KEY(order_id) REFERENCES orders(id)
    )""")

    # Дополнительные таблицы из твоих скриншотов
    cur.execute(
        "CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY AUTOINCREMENT, total REAL, profit REAL, date TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS debtors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, amount REAL, phone TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, event_text TEXT, event_date TEXT)")

    # Таблица настроек (для SMS и прочего)
    cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")

    # Базовые данные (пользователи)
    cur.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")
        cur.execute("INSERT INTO users (username, password, role) VALUES ('Samir', '1234', 'user')")

    # Базовые данные (Настройки SMS по умолчанию)
    cur.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('sms_target_phone', '+99360000000')")

    conn.commit()
    conn.close()


# === ТОВАРЫ ===
def get_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, purchase_price, selling_price, stock, min_stock, debt FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows
def add_product(name, category, purchase_price, selling_price, stock, min_stock):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, category, purchase_price, selling_price, stock, min_stock) VALUES (?, ?, ?, ?, ?, ?)",
                (name, category, float(purchase_price), float(selling_price), int(stock), int(min_stock)))
    conn.commit()
    conn.close()

def search_products(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, purchase_price, selling_price, stock, min_stock FROM products WHERE name LIKE ?", (f'%{query}%',))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_product(prod_id, name, category, purchase_price, selling_price, stock, min_stock):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE products SET name=?, category=?, purchase_price=?, selling_price=?, stock=?, min_stock=? WHERE id=?""",
                (name, category, float(purchase_price), float(selling_price), int(stock), int(min_stock), prod_id))
    conn.commit()
    conn.close()

def delete_product(prod_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (int(prod_id),))
    conn.commit()
    conn.close()

# === ЗАКАЗЫ И КОРЗИНА ===
def get_or_create_active_order():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM orders WHERE status = 'active' LIMIT 1")
    row = cur.fetchone()
    if row:
        order_id = row[0]
    else:
        cur.execute("INSERT INTO orders (status) VALUES ('active')")
        order_id = cur.lastrowid
        conn.commit()
    conn.close()
    return order_id

def add_item_to_order(order_id, product_id, product_name, quantity, price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, product_name, quantity, price))
    conn.commit()
    conn.close()

def get_current_basket_items(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, product_name, quantity, price, (quantity * price) as total FROM order_items WHERE order_id = ?", (order_id,))
    items = cur.fetchall()
    conn.close()
    return items

def remove_item_from_order(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM order_items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

def complete_order(order_id, customer_phone, total_amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = 'completed', customer_phone = ?, total_amount = ? WHERE id = ?", (customer_phone, total_amount, order_id))
    cur.execute("SELECT product_id, quantity FROM order_items WHERE order_id = ?", (order_id,))
    for item in cur.fetchall():
        cur.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item[1], item[0]))
    conn.commit()
    conn.close()

# === ПРОДАЖИ ===
def get_sales_today():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(total_amount) FROM orders WHERE date(sale_date) = date('now')")
    res = cur.fetchone()[0]
    conn.close()
    return res if res else 0.0

def get_sales_by_date(date_str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(total_amount) FROM orders WHERE date(sale_date) = ?", (date_str,))
    res = cur.fetchone()[0]
    conn.close()
    return res if res else 0.0

# === ДОЛЖНИКИ ===
def get_debtors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, amount, phone FROM debtors")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_debtor(name, amount, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO debtors (name, amount, phone) VALUES (?, ?, ?)", (name, amount, phone))
    conn.commit()
    conn.close()

def pay_debt(debtor_id, amount_paid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE debtors SET amount = amount - ? WHERE id = ?", (amount_paid, debtor_id))
    conn.commit()
    conn.close()

def delete_debtor(debtor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM debtors WHERE id=?", (debtor_id,))
    conn.commit()
    conn.close()

# === ПОЛЬЗОВАТЕЛИ ===
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Имя пользователя уже существует
    finally:
        conn.close()

def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def check_user_credentials(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# === НАСТРОЙКИ И SMS ===
def update_settings(key, value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_settings(key):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

def send_sms(message):
    # Умная функция: берет номер прямо из настроек базы!
    target_phone = get_settings("sms_target_phone")
    if not target_phone:
        print("❌ Ошибка: Номер телефона не задан в настройках!")
        return False

    print(f"📡 [СИМУЛЯЦИЯ SMS] Отправка на номер {target_phone}...")
    print(f"📩 Текст: {message}")
    print("✅ SMS успешно 'отправлено'!")
    return True

# === УТИЛИТЫ ===
def clear_database():
    conn = get_connection()
    cur = conn.cursor()
    tables = ['products', 'orders', 'order_items', 'sales', 'debtors', 'events']
    for t in tables:
        cur.execute(f"DELETE FROM {t}")
    conn.commit()
    conn.close()
def get_daily_sales():
    conn = sqlite3.connect("store_database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT SUM(total_amount) FROM orders
    WHERE status = 'completed' AND strftime('%Y-%m-%d', date) = datetime('now', 'localtime')""")
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0.0
def get_monthly_sales():
    conn = sqlite3.connect("store_database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT SUM(total_amount) FROM orders
    WHERE status = 'completed' AND strftime('%Y-%m-%d', date) = strftime('%Y-%m', 'now', 'localtime')""")
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0.0
def get_all_active_baskets():
    """Вспомогательная функция для получения ID всех открытых корзин"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM orders WHERE status = 'active'")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

def create_new_basket():
    """Создает новую чистую корзину в базе данных"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (status) VALUES ('active')")
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id

