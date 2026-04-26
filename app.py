import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, flash, g, make_response, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, instance_relative_config=True)
database_path = os.environ.get("DATABASE_PATH")
app.config["DATABASE"] = Path(database_path) if database_path else Path(app.instance_path) / "board.db"
app.secret_key = os.environ.get("SECRET_KEY", "dev")
PER_PAGE = 10
UPLOAD_FOLDER = Path("static/uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file):
    if not file or file.filename == "":
        return ""
    if not allowed_file(file.filename):
        return ""
    ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex[:12]}.{ext}"
    file.save(UPLOAD_FOLDER / filename)
    return f"/static/uploads/{filename}"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    db = get_db()
    with app.open_resource("schema.sql") as schema_file:
        db.executescript(schema_file.read().decode("utf8"))
    db.commit()


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Initialized the database.")


@app.before_request
def ensure_database_exists():
    if not Path(app.config["DATABASE"]).exists():
        init_db()


ORDER_MAP = {
    "newest": "id DESC",
    "oldest": "id ASC",
    "title": "title ASC",
}


@app.route("/")
def list_posts():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("q", "").strip()
    sort = request.args.get("sort", "newest")
    view = request.args.get("view", "list")
    if view not in ("list", "card"):
        view = "list"
    if sort not in ORDER_MAP:
        sort = "newest"
    order = ORDER_MAP[sort]
    db = get_db()
    if query:
        like = f"%{query}%"
        total = db.execute(
            "SELECT COUNT(*) FROM posts WHERE title LIKE ? OR content LIKE ?", (like, like)
        ).fetchone()[0]
        posts = db.execute(
            f"SELECT id, title, content, image_url, created_at FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY {order} LIMIT ? OFFSET ?",
            (like, like, PER_PAGE, (page - 1) * PER_PAGE),
        ).fetchall()
    else:
        total = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        posts = db.execute(
            f"SELECT id, title, content, image_url, created_at FROM posts ORDER BY {order} LIMIT ? OFFSET ?",
            (PER_PAGE, (page - 1) * PER_PAGE),
        ).fetchall()
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = max(1, min(page, total_pages))
    response = make_response(
        render_template("posts/list.html", posts=posts, page=page, total_pages=total_pages, query=query, sort=sort, view=view)
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def get_post_or_404(post_id):
    post = get_db().execute(
        "SELECT id, title, content, image_url, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()
    if post is None:
        abort(404)
    return post


def save_post(title, content, image_url=""):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    db = get_db()
    db.execute(
        "INSERT INTO posts (title, content, image_url, created_at) VALUES (?, ?, ?, ?)",
        (title, content, image_url, created_at),
    )
    db.commit()


@app.route("/posts/new", methods=["GET", "POST"])
@app.route("/posts/new/", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        return render_template("posts/create.html", post=None, form_action=url_for("new_post"), submit_label="Publish")

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    image_url = request.form.get("image_url", "").strip()
    image_file = request.files.get("image")

    if not title and not content:
        flash("제목 또는 내용을 입력해 주세요.")
        return render_template(
            "posts/create.html",
            post={"title": title, "content": content, "image_url": image_url},
            form_action=url_for("new_post"),
            submit_label="Publish",
        ), 400

    if not title:
        title = "(제목 없음)"

    uploaded = save_uploaded_image(image_file)
    if uploaded:
        image_url = uploaded

    save_post(title, content, image_url)
    flash("게시글이 등록되었습니다.")
    return redirect(url_for("list_posts"))


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = get_post_or_404(post_id)
    return render_template("posts/detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = get_post_or_404(post_id)
    return render_template(
        "posts/create.html",
        post=post,
        form_action=url_for("update_post", post_id=post_id),
        submit_label="Update",
    )


@app.route("/posts/<int:post_id>/update", methods=["POST"])
def update_post(post_id):
    get_post_or_404(post_id)
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    image_url = request.form.get("image_url", "").strip()
    image_file = request.files.get("image")
    remove_image = request.form.get("remove_image")

    if not title and not content:
        flash("제목 또는 내용을 입력해 주세요.")
        return redirect(url_for("edit_post", post_id=post_id))

    if not title:
        title = "(제목 없음)"

    uploaded = save_uploaded_image(image_file)
    if uploaded:
        image_url = uploaded
    elif remove_image:
        image_url = ""

    db = get_db()
    db.execute(
        "UPDATE posts SET title = ?, content = ?, image_url = ? WHERE id = ?",
        (title, content, image_url, post_id),
    )
    db.commit()
    flash("게시글이 수정되었습니다.")
    return redirect(url_for("post_detail", post_id=post_id))


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = get_post_or_404(post_id)
    if post["image_url"] and post["image_url"].startswith("/static/uploads/"):
        img_path = Path(post["image_url"].lstrip("/"))
        if img_path.exists():
            img_path.unlink()
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    flash("게시글이 삭제되었습니다.")
    return redirect(url_for("list_posts"))


@app.route("/posts", methods=["GET", "POST"])
@app.route("/posts/", methods=["GET", "POST"])
@app.route("/posts/new에서", methods=["GET", "POST"])
def create_post_legacy():
    if request.method == "GET":
        return redirect(url_for("new_post"))

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title and not content:
        flash("제목 또는 내용을 입력해 주세요.")
        return redirect(url_for("new_post"))

    if not title:
        title = "(제목 없음)"

    save_post(title, content)
    flash("게시글이 등록되었습니다.")
    return redirect(url_for("list_posts"))


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)
