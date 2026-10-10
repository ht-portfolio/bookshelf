# db.py：DB処理

import sqlite3
from pathlib    import Path
from models     import Book

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "bookshelf.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE,
            title TEXT NOT NULL,
            author TEXT,
            publisher TEXT,
            published_date TEXT,
            status INTEGER NOT NULL DEFAULT 0
                CHECK (status IN (0, 1, 2)),
            memo TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")

# Bookオブジェクトを受け取り、booksテーブルに追加する。
def add_book(book: Book):
    # SQLite へ接続
    conn = get_connection()

    # booksテーブルへレコードを追加
    cursor = conn.execute(
        """
        INSERT INTO books (
            isbn,
            title,
            author,
            publisher,
            published_date,
            status,
            memo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            book.isbn or None,
            book.title,
            book.author,
            book.publisher,
            book.published_date,
            book.status,
            book.memo,
        )
    )
    # コミット
    conn.commit()
    # 自動採番されたidを取得し、bookオブジェクトのidに設定する。
    book.id = cursor.lastrowid
    # SQLite との接続を閉じる
    conn.close()
    return book

def get_all_books():
    # SQLiteへ接続。
    conn = get_connection()

    # booskテーブルの全レコードを取得。
    rows = conn.execute(
        """
        SELECT
            id,
            isbn,
            title,
            author,
            publisher,
            published_date,
            status,
            memo,
            created_at,
            updated_at
        FROM books
        ORDER BY id DESC
        """
    ).fetchall()
    # SQLiteとの接続を解除。
    conn.close()
    
    # 各レコードをBookオブジェクトへ変換。
    books = [
        Book(
            id      = row["id"],
            isbn    = row["isbn"],
            title   = row["title"],
            author  = row["author"],
            publisher       = row["publisher"],
            published_date  = row["published_date"],
            status  = row["status"],
            memo    = row["memo"],
            created_at  = row["created_at"],
            updated_at  = row["updated_at"],
        )
        for row in rows
    ]
    return books

if __name__ == "__main__":
    init_db()
