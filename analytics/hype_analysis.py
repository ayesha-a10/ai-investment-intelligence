import pandas as pd
from data_pipeline.database import get_connection


def calculate_hype():
    conn = get_connection()

    news_topics = pd.read_sql("SELECT * FROM news_topics", conn)

    topic_counts = (
        news_topics["topic"]
        .value_counts()
        .reset_index()
    )

    topic_counts.columns = ["topic", "article_count"]

    total_articles = topic_counts["article_count"].sum()

    topic_counts["hype_score"] = (
        topic_counts["article_count"] / total_articles
    )

    topic_counts = topic_counts.sort_values(
        by="hype_score", ascending=False
    )

    topic_counts.to_sql(
        "hype_scores",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Hype analysis completed.")
    print(topic_counts)


if __name__ == "__main__":
    calculate_hype()