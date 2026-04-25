import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, flash, g, make_response, redirect, render_template, request, url_for

app = Flask(__name__, instance_relative_config=True)
database_path = os.environ.get("DATABASE_PATH")
app.config["DATABASE"] = Path(database_path) if database_path else Path(app.instance_path) / "board.db"
app.secret_key = os.environ.get("SECRET_KEY", "dev")


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


@app.route("/")
def list_posts():
    posts = get_db().execute(
        "SELECT id, title, content, created_at FROM posts ORDER BY id DESC"
    ).fetchall()
    response = make_response(render_template("posts/list.html", posts=posts))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def get_post_or_404(post_id):
    post = get_db().execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()
    if post is None:
        abort(404)
    return post


def save_post(title, content):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    db = get_db()
    db.execute(
        "INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
        (title, content, created_at),
    )
    db.commit()


@app.route("/posts/new", methods=["GET", "POST"])
@app.route("/posts/new/", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        return render_template("posts/create.html", post=None, form_action=url_for("new_post"), submit_label="Publish")

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title and not content:
        flash("제목 또는 내용을 입력해 주세요.")
        return render_template(
            "posts/create.html",
            post={"title": title, "content": content},
            form_action=url_for("new_post"),
            submit_label="Publish",
        ), 400

    if not title:
        title = "(제목 없음)"

    save_post(title, content)
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

    if not title and not content:
        flash("제목 또는 내용을 입력해 주세요.")
        return redirect(url_for("edit_post", post_id=post_id))

    if not title:
        title = "(제목 없음)"

    db = get_db()
    db.execute(
        "UPDATE posts SET title = ?, content = ? WHERE id = ?",
        (title, content, post_id),
    )
    db.commit()
    flash("게시글이 수정되었습니다.")
    return redirect(url_for("post_detail", post_id=post_id))


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    get_post_or_404(post_id)
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
