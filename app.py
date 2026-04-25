import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, g, make_response, redirect, render_template, request, url_for

app = Flask(__name__, instance_relative_config=True)
app.config["DATABASE"] = Path(app.instance_path) / "board.db"
app.secret_key = "dev"


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
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
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
        return render_template("posts/create.html")

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("제목과 내용을 모두 입력해 주세요.")
        return render_template("posts/create.html", title=title, content=content), 400

    save_post(title, content)
    flash("게시글이 등록되었습니다.")
    return redirect(url_for("list_posts"))


@app.route("/posts", methods=["GET", "POST"])
@app.route("/posts/", methods=["GET", "POST"])
@app.route("/posts/new에서", methods=["GET", "POST"])
def create_post_legacy():
    if request.method == "GET":
        return redirect(url_for("new_post"))

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("제목과 내용을 모두 입력해 주세요.")
        return redirect(url_for("new_post"))

    save_post(title, content)
    flash("게시글이 등록되었습니다.")
    return redirect(url_for("list_posts"))


if __name__ == "__main__":
    app.run(debug=True)
