import sqlite3
import json
from datetime import datetime, timedelta
from config import DEMO_ITEMS

DATABASE_PATH = "subscriptions.db"

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            subscription_plan TEXT,
            subscription_expiry TEXT,
            is_active INTEGER DEFAULT 0,
            joined_at TEXT,
            last_active TEXT,
            language TEXT DEFAULT 'en'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan TEXT,
            amount REAL,
            currency TEXT,
            payment_method TEXT,
            transaction_id TEXT,
            status TEXT,
            created_at TEXT,
            verified_by INTEGER,
            verified_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            item_data TEXT,
            price REAL,
            status TEXT DEFAULT 'active',
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ---- User functions ----
def get_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "user_id": user[0],
            "username": user[1],
            "first_name": user[2],
            "subscription_plan": user[3],
            "subscription_expiry": user[4],
            "is_active": user[5],
            "joined_at": user[6],
            "last_active": user[7],
            "language": user[8] if len(user) > 8 else 'en'
        }
    return None

def create_user(user_id, username, first_name, language='en'):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, is_active, joined_at, last_active, language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, 0, datetime.now().isoformat(), datetime.now().isoformat(), language))
    conn.commit()
    conn.close()

def set_user_language(user_id, language):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
    conn.commit()
    conn.close()

def get_user_language(user_id):
    user = get_user(user_id)
    return user['language'] if user else 'en'

def add_payment_record(user_id, plan_key, amount, method, transaction_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO payments (user_id, plan, amount, currency, payment_method, transaction_id, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, plan_key, amount, "USD", method, transaction_id, "pending", datetime.now().isoformat()))
    conn.commit()
    conn.close()

# ---- Inventory functions ----
def get_active_items(category):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, item_data, price, status FROM inventory
        WHERE category = ? AND status = 'active'
    ''', (category,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_item_by_id(item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, category, item_data, price, status FROM inventory
        WHERE id = ?
    ''', (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'id': row[0],
            'category': row[1],
            'item_data': json.loads(row[2]),
            'price': row[3],
            'status': row[4]
        }
    return None

def mark_item_sold(item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE inventory SET status = "sold" WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

def populate_inventory():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventory")
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return
    for category, items in DEMO_ITEMS.items():
        for item in items:
            price = item.pop('price')  # remove price from item_data
            cursor.execute('''
                INSERT INTO inventory (category, item_data, price, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (category, json.dumps(item), price, 'active', datetime.now().isoformat()))
    conn.commit()
    conn.close()