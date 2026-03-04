import pandas as pd
from data_pipeline.database import get_connection


def calculate_emerging_score():
    conn = get_connection()

    hype = pd.read_sql("SELECT * FROM hype_scores", conn)
    capital = pd.read_sql("SELECT * FROM capital_distribution", conn)

    # Late stage capital share
    late_stage = capital[
        capital["funding_stage"].isin(["IPO", "Series C"])
    ]["capital_share"].sum()

    # Compute emerging multiplier
    multiplier = 1 - late_stage

    hype["emerging_score"] = hype["hype_score"] * multiplier

    hype = hype.sort_values(by="emerging_score", ascending=False)

    hype.to_sql(
        "emerging_opportunities",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Emerging opportunity scores calculated.")
    print(hype)


if __name__ == "__main__":
    calculate_emerging_score()