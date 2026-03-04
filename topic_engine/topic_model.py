import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from data_pipeline.database import get_connection


def run_topic_modeling():
    conn = get_connection()

    df = pd.read_sql("SELECT * FROM clean_news", conn)
    print("Total documents for modeling:", len(df))

    documents = df["clean_text"].tolist()

    # Lightweight embedding model
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Replace HDBSCAN with KMeans
    cluster_model = KMeans(n_clusters=8, random_state=42)

    topic_model = BERTopic(
        embedding_model=embedding_model,
        hdbscan_model=cluster_model,
        calculate_probabilities=False,
        verbose=True
    )

    topics, _ = topic_model.fit_transform(documents)

    df["topic"] = topics

    # Store results
    df[["id", "topic"]].to_sql(
        "news_topics",
        conn,
        if_exists="replace",
        index=False
    )

    topic_info = topic_model.get_topic_info()

    # Convert any non-primitive columns to string
    for col in topic_info.columns:
        if topic_info[col].apply(lambda x: isinstance(x, (list, dict))).any():
            topic_info[col] = topic_info[col].astype(str)

    topic_info.to_sql(
        "topic_summary",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Topic modeling completed successfully.")


if __name__ == "__main__":
    run_topic_modeling()