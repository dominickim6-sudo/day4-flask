from crawler import fetch_news
from datetime import datetime
from pathlib import Path

import os
import sqlite3


def seed(database_path=None):
    if not database_path:
        database_path = os.environ.get("DATABASE_PATH")
    db_path = Path(database_path) if database_path else Path("instance/board.db")

    try:
        news = fetch_news(limit=10)
    except Exception as e:
        print(f"뉴스 가져오기 실패: {e}")
        return

    if not news:
        print("가져온 뉴스가 없습니다.")
        return

    conn = sqlite3.connect(db_path)
    added = 0

    for article in news:
        exists = conn.execute(
            "SELECT 1 FROM posts WHERE title = ?", (article["title"],)
        ).fetchone()
        if exists:
            continue

        conn.execute(
            "INSERT INTO posts (title, content, image_url, created_at) VALUES (?, ?, '', ?)",
            (article["title"], article["summary"] or article["link"], article["pub_date"]),
        )
        added += 1

    conn.commit()
    conn.close()
    print(f"{added}건 추가됨 ({len(news) - added}건 중복 건너뜀)")


if __name__ == "__main__":
    seed()
