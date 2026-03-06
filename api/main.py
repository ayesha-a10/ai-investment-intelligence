from fastapi import FastAPI
import pandas as pd
from data_pipeline.database import get_connection
from data_pipeline.funding_ingest import create_funding_table
from data_pipeline.patent_ingest import create_patent_table
from analytics.hype_score import create_hype_table


app = FastAPI()


def get_table(table_name: str):
    conn = get_connection()
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()
        

@app.on_event("startup")
def startup_event():
    print("Creating database tables...")

    create_funding_table()
    create_patent_table()
    create_hype_table()

    print("Tables ready.")


@app.get("/")
def dashboard():

    hype = get_table("hype_scores")
    funding = get_table("funding")
    patents = get_table("patents")

    return {
        "status": "AI Investment Intelligence API Running",
        "hype_scores": hype.to_dict(orient="records"),
        "funding": funding.to_dict(orient="records"),
        "patents": patents.to_dict(orient="records"),
    }


@app.get("/health")
def health():
    return {"status": "ok"}
