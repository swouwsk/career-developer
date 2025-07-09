import sqlite3
from main import *
from config import *


def init_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            step INTEGER DEFAULT 0,
            IT INTEGER DEFAULT 0,
            Creativity INTEGER DEFAULT 0,
            Social INTEGER DEFAULT 0,
            Medicine INTEGER DEFAULT 0,
            Technical INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Создание пользователя, если нет
def create_user_if_not_exists(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not c.fetchone():
        c.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
