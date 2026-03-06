from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from data_pipeline.database import get_connection
from data_pipeline.funding_ingest import create_funding_table, ingest_funding
from data_pipeline.preprocess_news import preprocess_news
from analytics.hype_analysis import calculate_hype
from analytics.capital_analysis import calculate_capital_distribution
from analytics.emerging_score import calculate_emerging_score

app = FastAPI(title="AI Investment Intelligence API")

@app.on_event("startup")
def initialize_pipeline():
    print("Starting pipeline initialization...")

    try:
        create_funding_table()
        ingest_funding()
        preprocess_news()
        calculate_hype()
        calculate_capital_distribution()
        calculate_emerging_score()

        print("Pipeline initialized successfully.")

    except Exception as e:
        print("Startup error:", e)

templates = Jinja2Templates(directory="api/templates")


def get_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


@app.get("/topics")
def get_topics():
    return get_table("topic_summary").to_dict(orient="records")


@app.get("/hype")
def get_hype():
    return get_table("hype_scores").to_dict(orient="records")


@app.get("/capital")
def get_capital():
    return get_table("capital_distribution").to_dict(orient="records")


@app.get("/emerging")
def get_emerging():
    return get_table("emerging_opportunities").to_dict(orient="records")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    hype = get_table("hype_scores")
    capital = get_table("capital_distribution")
    emerging = get_table("emerging_opportunities")

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "hype": hype.to_dict(orient="records"),
            "capital": capital.to_dict(orient="records"),
            "emerging": emerging.to_dict(orient="records"),
        },
    )
