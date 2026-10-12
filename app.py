# app.py 

from flask  import Flask, render_template, request
from db     import add_book, get_all_books, get_book_by_id, update_book
from models import Book

app = Flask(__name__)

@app.route("/")
def index():
    return "Bookshelf application is running."

@app.route("/books/new", methods=["GET","POST"])
def new_book():
    if request.method == "POST":
        # request.form から値を取得し、bookオブジェクトを作成する。
        book = Book(
            isbn = request.form.get("isbn") or None,
            title= request.form.get("title", ""),
            author = request.form.get("author") or None,
            publisher= request.form.get("publisher") or None,
            published_date= request.form.get("published_date") or None,
            status= request.form.get("status", 0),
            memo = request.form.get("memo") or None,
        )
        # DBへ登録する。
        add_book(book)
        return f"書籍を登録しました。ID: {book.id}"
    return render_template("book_form.html")

@app.route("/books")
def book_list():
    books = get_all_books()
    return render_template("book_list.html", books=books)

@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = get_book_by_id(book_id)

    if book is None:
        return "指定された書籍は存在しません。", 404
    return render_template("book_detail.html", book=book)

@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = get_book_by_id(book_id)
    print("DEBUG author:", book.author)

    if book is None:
        return "指定された書籍は存在しません。", 404

    if request.method == "POST":
        # フォームの入力値を取得し、bookオブジェクトに格納する。
        book.isbn   = request.form.get("isbn") or None
        book.title  = request.form.get("title","") 
        book.author = request.form.get("author") or None
        book.publisher      = request.form.get("publisher") or None
        book.published_date = request.form.get("publisher_date") or None
        book.status = int( request.form.get("status", 0))
        book.memo   = request.form.get("memo") or None
        # レコードを更新する。
        update_book(book)
        return f"書籍を更新しました。ID： {book.id}"

    return render_template("book_edit.html", book=book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
