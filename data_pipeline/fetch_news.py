import requests
import os
import time
from dotenv import load_dotenv
from database import create_news_table, get_connection

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
URL = "https://newsapi.org/v2/everything"

QUERY = "AI startup OR generative AI OR robotics OR AI funding"


def fetch_news(pages=5):
    if not API_KEY:
        print("ERROR: NEWS_API_KEY not found in .env file")
        return

    create_news_table()

    conn = get_connection()
    cursor = conn.cursor()

    total_inserted = 0

    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")

        params = {
            "q": QUERY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,
            "page": page,
            "apiKey": API_KEY
        }

        response = requests.get(URL, params=params)
        data = response.json()

        if data.get("status") != "ok":
            print("API Error:", data)
            break

        articles = data.get("articles", [])

        for article in articles:
            try:
                cursor.execute("""
                    INSERT INTO news_articles 
                    (title, description, content, published_at, source, url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    article.get("title"),
                    article.get("description"),
                    article.get("content"),
                    article.get("publishedAt"),
                    article.get("source", {}).get("name"),
                    article.get("url")
                ))
                total_inserted += 1

            except:
                # Skip duplicates (due to UNIQUE url constraint)
                pass

        time.sleep(1)  # Prevent rate limit issues

    conn.commit()
    conn.close()

    print(f"Inserted {total_inserted} new records into database.")


if __name__ == "__main__":
    fetch_news(pages=10)