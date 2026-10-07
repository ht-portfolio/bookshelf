from dataclasses import dataclass


@dataclass
class Book:
    id: int | None = None
    isbn: str | None = None
    title: str = ""
    author: str | None = None
    publisher: str | None = None
    published_date: str | None = None
    status: int = 0
    memo: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
