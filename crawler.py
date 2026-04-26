import requests
from bs4 import BeautifulSoup
from datetime import datetime

RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"


def fetch_news(limit=10):
    resp = requests.get(RSS_URL, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "xml")
    items = soup.find_all("item")[:limit]

    news = []
    for item in items:
        title = item.find("title").text if item.find("title") else ""
        link = item.find("link").text if item.find("link") else ""
        pub_date = item.find("pubDate").text if item.find("pubDate") else ""
        summary = item.find("description").text if item.find("description") else ""

        if pub_date:
            try:
                dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S GMT")
                pub_date = dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass

        # strip HTML tags from summary
        if summary:
            summary = BeautifulSoup(summary, "html.parser").get_text(strip=True)

        news.append({
            "title": title,
            "summary": summary[:100] + ("..." if len(summary) > 100 else ""),
            "link": link,
            "pub_date": pub_date,
        })

    return news


def print_news(news_list):
    print(f"\n{'='*60}")
    print(f"  구글 뉴스 한국어 RSS — 최신 {len(news_list)}건")
    print(f"{'='*60}\n")

    for i, n in enumerate(news_list, 1):
        print(f"[{i}] {n['title']}")
        print(f"    시간 : {n['pub_date']}")
        print(f"    요약 : {n['summary']}")
        print(f"    링크 : {n['link']}")
        print()


if __name__ == "__main__":
    articles = fetch_news(limit=10)
    print_news(articles)
