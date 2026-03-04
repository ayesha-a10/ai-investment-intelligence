import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
URL = "https://newsapi.org/v2/everything"

QUERY = "AI startup OR generative AI OR robotics OR AI funding"

def fetch_news(pages=5):
    all_records = []

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

        if data["status"] != "ok":
            print("Error:", data)
            break

        articles = data["articles"]

        for article in articles:
            all_records.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "published_at": article.get("publishedAt"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url")
            })

        time.sleep(1)  # avoid hitting rate limit

    df = pd.DataFrame(all_records)

    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv("data/raw_news.csv", index=False)
    print(f"Saved {len(df)} articles.")

if __name__ == "__main__":
    fetch_news(pages=10)