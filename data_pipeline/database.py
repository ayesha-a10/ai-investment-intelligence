import sqlite3

DB_PATH = "data/ai_investment.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_news_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            content TEXT,
            published_at TEXT,
            source TEXT,
            url TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()