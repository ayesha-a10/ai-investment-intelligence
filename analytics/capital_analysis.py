import pandas as pd
from data_pipeline.database import get_connection


def calculate_capital_distribution():
    conn = get_connection()

    funding = pd.read_sql("SELECT * FROM funding_data", conn)

    stage_counts = (
        funding.groupby("funding_stage")["amount_usd"]
        .sum()
        .reset_index()
    )

    total_capital = stage_counts["amount_usd"].sum()

    stage_counts["capital_share"] = (
        stage_counts["amount_usd"] / total_capital
    )

    stage_counts = stage_counts.sort_values(
        by="capital_share", ascending=False
    )

    stage_counts.to_sql(
        "capital_distribution",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Capital distribution calculated.")
    print(stage_counts)


if __name__ == "__main__":
    calculate_capital_distribution()