import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

URL = "https://newsapi.org/v2/everything"

params = {
    "q": "AI startup OR generative AI OR robotics OR AI funding",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 100,
    "apiKey": API_KEY
}

def fetch_news():
    response = requests.get(URL, params=params)
    data = response.json()

    if data["status"] != "ok":
        print("Error fetching data:", data)
        return

    articles = data["articles"]

    records = []

    for article in articles:
        records.append({
            "title": article["title"],
            "description": article["description"],
            "content": article["content"],
            "published_at": article["publishedAt"],
            "source": article["source"]["name"],
            "url": article["url"]
        })

    df = pd.DataFrame(records)

    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv("data/raw_news.csv", index=False)

    print("News data saved successfully.")

if __name__ == "__main__":
    fetch_news()