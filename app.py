# app.py 

from flask  import Flask, render_template, request
from db     import add_book
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
