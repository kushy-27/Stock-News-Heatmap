import json
from fastapi import APIRouter, Query # type: ignore

router = APIRouter()
ARTICLES = "data/processed/articles_with_confidence.json"

@router.get("/by-sector")
def news_by_sector(
    sector: str,
    limit: int = 20
):
    with open(ARTICLES) as f:
        articles = json.load(f)

    filtered = [
        a for a in articles
        if sector in a.get("sectors", [])
    ]

    filtered.sort(
        key=lambda x: (x.get("confidence",0), x.get("fetched_at","")),
        reverse=True
    )

    return filtered[:limit]
