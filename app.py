# app.py 

from flask  import Flask, render_template, request, redirect, url_for
from db     import (
    add_book,
    get_all_books,
    get_book_by_id,
    update_book,
    delete_book,
    serach_books,
)
from models     import Book
from datetime   import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return "Bookshelf application is running."

@app.route("/books/new", methods=["GET","POST"])
def new_book():
    if request.method == "POST":
        # 入力値チェック
        errors = validate_book_form(request.form)
        if errors:
            return render_template(
                "book_form.html",
                errors = errors,
                form_data = request.form,
            )

        # request.form から値を取得し、bookオブジェクトを作成する。
        book = Book(
            isbn    = request.form.get("isbn", "").strip() or None,
            title   = request.form.get("title", "").strip(),
            author  = request.form.get("author", "").strip() or None,
            publisher= request.form.get("publisher", "").strip() or None,
            published_date= request.form.get("published_date", "").strip() or None,
            status  = request.form.get("status", 0),
            memo    = request.form.get("memo", "").strip() or None,
        )

        # DBへ登録する。
        add_book(book)

        # return f"書籍を登録しました。ID: {book.id}"
        return redirect(url_for("book_list"))

    return render_template(
        "book_form.html",
        errors = [],
        form_data = {},
    )

@app.route("/books")
def book_list():
    keyword     = request.args.get("keyword", "").strip()
    status_text = request.args.get("status", "").strip()
    sort        = request.args.get("sort", "newest").strip()
    print("DEBUG sort:", sort)

    if status_text in ("0", "1", "2"):
        status = int(status_text)
    else:
        status = None

    if sort not in ("newest", "oldest", "title", "published"):
        sort = "newest"

    if keyword or status is not None or sort != "newest":
        # キーワードあり
        books = serach_books(keyword, status, sort)
    else:
        # キーワードなし（全権取得）
        books = get_all_books()

    return render_template(
        "book_list.html",
        books   = books,
        keyword = keyword,
        status  = status,
        sort    = sort,
    )

@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = get_book_by_id(book_id)

    if book is None:
        return "指定された書籍は存在しません。", 404
    return render_template("book_detail.html", book=book)

@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = get_book_by_id(book_id)

    if book is None:
        return "指定された書籍は存在しません。", 404

    if request.method == "POST":
        # 入力値チェック
        errors = validate_book_form(request.form)
        if errors:
            return render_template(
                "book_form.html",
                errors = errors,
                form_data = request.form,
            )

        # フォームの入力値を取得し、bookオブジェクトに格納する。
        book.isbn   = request.form.get("isbn", "").strip() or None
        book.title  = request.form.get("title","").strip()
        book.author = request.form.get("author", "").strip() or None
        book.publisher      = request.form.get("publisher", "").strip() or None
        book.published_date = request.form.get("published_date", "").strip() or None
        book.status = int( request.form.get("status", 0))
        book.memo   = request.form.get("memo").strip() or None

        # レコードを更新する。
        update_book(book)
        
        # return f"書籍を更新しました。ID： {book.id}"
        return redirect(url_for("book_list"))

    return render_template("book_edit.html", book=book)

@app.route("/books/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book_view(book_id):
    book = get_book_by_id(book_id)

    if book is None:
        return "指定された書籍は存在しません。", 404
    
    if request.method == "POST":
        delete_book(book_id)
        return redirect(url_for("book_list"))

    return render_template("book_delete.html", book=book)

def validate_book_form(form):
    errors = []

    title   = form.get("title","").strip()
    isbn    = form.get("isbn","").strip()
    author  = form.get("author","").strip()
    publisher       = form.get("publisher","").strip()
    published_date  = form.get("published_date","").strip()
    status_text     = form.get("status","").strip()
    memo    = form.get("memo","").strip()

    # 入力値チェック
    if not title:
        errors.append("書名は必須です。")
    elif len(title) > 200:
        errors.append("書名は200文字以内で入力してください。")
    
    if len(isbn) > 20:
        errors.append("ISBNは20文字以内で入力してください。")

    if len(author) > 200:
        errors.append("著者名は200文字以内で入力してください。")

    if len(publisher) > 200:
        errors.append("出版社名は200文字以内で入力してください。")

    if published_date :
        try:
            datetime.strptime(published_date, "%Y-%m-%d")
        except ValueError:
            errors.append("出版日は正しい日付で入力してください。")

    if len(memo) > 2000:
        errors.append("メモは2000文字以内で入力してください。")

    if status_text not in ("0", "1", "2"):
        errors.append("読書状態が不正です。")

    return errors
    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
