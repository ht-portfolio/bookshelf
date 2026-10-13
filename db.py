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

# booskテーブルの全レコードを取得し、booksオブジェクトを返す。
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

def get_book_by_id(book_id: int):
    # SQLiteへ接続。
    conn = get_connection()

    # 検索し該当の一件を取得する。
    row = conn.execute(
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
        WHERE id = ?
        """,
        (book_id,),
    ).fetchone()

    # SQLiteの接続を解除。
    conn.close()

    # 検索の結果、該当なしの場合はNoneを、該当があれば検索結果の先頭１レコードを返す。
    if row is None:
        return None
    return Book(
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

def update_book(book: Book):
    conn = get_connection()

    conn.execute(
        """
        UPDATE books
        SET
            isbn    = ?,
            title   = ?,
            author  = ?,
            publisher       = ?,
            published_date  = ?,
            status  = ?,
            memo    = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            book.isbn or None,
            book.title,
            book.author,
            book.publisher,
            book.published_date,
            book.status,
            book.memo,
            book.id,
        ),
    )
    conn.commit()
    conn.close()

def delete_book(book_id: int):
    conn = get_connection()
    conn.execute(
        """
        DELETE FROM books
        WHERE id = ?
        """,
        (book_id,),
    )
    conn.commit()
    conn.close()

def serach_books(keyword: str):
    conn = get_connection()

    serach_word = f"%{keyword}%"

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
        WHERE
            title       LIKE ?
            OR author   LIKE ?
            OR isbn     LIKE ?
            OR publisher LIKE ?
        ORDER BY id DESC
        """,
        (
            serach_word,
            serach_word,
            serach_word,
            serach_word,
        ),
    ).fetchall()
    conn.close()

    return [
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

if __name__ == "__main__":
    init_db()
