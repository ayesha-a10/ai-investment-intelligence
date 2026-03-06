from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.express as px

from data_pipeline.database import get_connection

app = FastAPI()

templates = Jinja2Templates(directory="api/templates")


def get_table(table_name: str):
    conn = get_connection()
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    hype = get_table("hype_scores")

    if hype.empty:
        chart_html = "<h3>No data available</h3>"
    else:
        fig = px.bar(
            hype,
            x="topic",
            y="hype_score",
            title="AI Topic Hype Scores",
        )

        chart_html = fig.to_html(full_html=False)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "chart": chart_html,
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}
