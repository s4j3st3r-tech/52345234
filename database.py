import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        text TEXT DEFAULT 'WATERMARK',
        position TEXT DEFAULT 'Снизу-Справа',
        color TEXT DEFAULT 'Белый',
        font TEXT DEFAULT 'Roboto',
        transparency INTEGER DEFAULT 180,
        size INTEGER DEFAULT 40
    )''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cur.fetchone()
    conn.close()
    return user

def update_user(user_id, field, value):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, user_id))
    conn.commit()
    conn.close()
