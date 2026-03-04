import pandas as pd
import re
from database import get_connection


def clean_text(text):
    if pd.isnull(text):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # remove special chars
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_news():
    conn = get_connection()

    df = pd.read_sql("SELECT * FROM news_articles", conn)

    print("Total raw articles:", len(df))

    df["full_text"] = (
        df["title"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["content"].fillna("")
    )

    df["clean_text"] = df["full_text"].apply(clean_text)

    df = df[df["clean_text"].str.len() > 50]

    print("After cleaning:", len(df))

    df[["id", "clean_text"]].to_sql(
        "clean_news",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Cleaned news stored in clean_news table.")


if __name__ == "__main__":
    preprocess_news()