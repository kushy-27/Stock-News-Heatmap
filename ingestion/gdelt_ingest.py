import os
import requests
import json
from datetime import datetime

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

PARAMS = {
    "query": '("stock market" OR "share price" OR "equity market") AND sourcecountry:india',
    "mode": "ArtList",
    "format": "json",
    "maxrecords": 200,
    "sort": "DateDesc",
    "timespan": "2d",
    "sourcelang": "English"
}


def fetch_news():
    response = requests.get(GDELT_URL, params=PARAMS, timeout=15)

    response.raise_for_status()

    ct = (response.headers.get("Content-Type") or "").lower()
    if "json" not in ct:
        raise RuntimeError("Response is not JSON. Likely HTML error/blocked. See printed snippet above.")

    return response.json()


def parse_articles(data):
    articles = []
    
    for item in data.get("articles", []):
        source = (
    item.get("source")
    or item.get("domain")
    or item.get("sourceCollection")
    or item.get("sourceCountry")
    or item.get("language")
)
        articles.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "source": source,
            "published": item.get("seendate"),
            "fetched_at": datetime.utcnow().isoformat()
        })
    
    seen = set()
    unique = []
    for a in articles:
        u = a["url"]
        if u and u not in seen:
            seen.add(u)
            unique.append(a)
    return unique

if __name__ == "__main__":
    raw_data = fetch_news()
    articles = parse_articles(raw_data)

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/gdelt_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
