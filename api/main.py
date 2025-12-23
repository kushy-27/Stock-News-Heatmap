from fastapi import FastAPI # type: ignore
from fastapi.responses import FileResponse # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from api.routes import sectors, news, tickers
import json
import os
from pathlib import Path

app = FastAPI(title="Stock News Heatmap API")

BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = BASE_DIR / "UI"

print(f"BASE_DIR: {BASE_DIR}")
print(f"UI_DIR: {UI_DIR}")
print(f"UI_DIR exists: {UI_DIR.exists()}")

app.mount("/UI", StaticFiles(directory=str(UI_DIR)), name="UI")

@app.get("/")
def dashboard():
    return FileResponse(str(UI_DIR / "dashboard.html"))

@app.get("/news/by-sector")
def news_by_sector(sector: str):
    # Also fix this path to be relative to BASE_DIR
    data_file = BASE_DIR / "data" / "processed" / "articles_with_confidence.json"
    with open(data_file) as f:
        articles = json.load(f)

    return [
        {
            "title": a["title"],
            "sentiment": a["sentiment_compound"],
            "confidence": a["confidence"],
            "source": a["source"]
        }
        for a in articles
        if sector in a.get("sectors", [])
    ][:20]

app.include_router(sectors.router, prefix="/sectors", tags=["sectors"])
app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(tickers.router, prefix="/tickers", tags=["tickers"])
