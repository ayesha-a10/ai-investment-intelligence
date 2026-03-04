import pandas as pd
from database import get_connection

CSV_PATH = "data/raw_funding.csv"


def create_funding_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funding_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_name TEXT,
            industry TEXT,
            country TEXT,
            funding_stage TEXT,
            amount_usd REAL,
            funding_date TEXT,
            employees INTEGER
        )
    """)

    conn.commit()
    conn.close()


def ingest_funding():
    df = pd.read_csv(CSV_PATH)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert date
    df["Funding Date"] = pd.to_datetime(df["Funding Date"], errors="coerce")

    # Drop rows without funding amount
    df = df.dropna(subset=["Amount Raised (USD)"])

    # OPTIONAL: Filter only AI-related startups
    ai_keywords = ["AI", "Artificial Intelligence", "Machine Learning", "Robotics"]

    df_ai = df[df["Industry"].str.contains("|".join(ai_keywords), case=False, na=False)]

    print(f"Total AI-related funding records: {len(df_ai)}")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df_ai.iterrows():
        cursor.execute("""
            INSERT INTO funding_data
            (startup_name, industry, country, funding_stage, amount_usd, funding_date, employees)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Startup Name"],
            row["Industry"],
            row["Country"],
            row["Funding Stage"],
            row["Amount Raised (USD)"],
            row["Funding Date"].strftime("%Y-%m-%d") if not pd.isnull(row["Funding Date"]) else None,
            row["Number of Employees"]
        ))

    conn.commit()
    conn.close()

    print("Funding data inserted successfully.")


if __name__ == "__main__":
    create_funding_table()
    ingest_funding()