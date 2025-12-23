import json, os
from datetime import datetime, timezone

SRC_SECTOR = "data/processed/sector_sentiment_heatmap.json"
SRC_TICKER = "data/processed/ticker_sentiment_heatmap.json"

BASE = "storage"

def save_snapshot():
    now = datetime.now(timezone.utc)
    hour_key = now.strftime("%Y-%m-%d-%H")
    day_key  = now.strftime("%Y-%m-%d")

    os.makedirs(f"{BASE}/latest", exist_ok=True)
    os.makedirs(f"{BASE}/hourly", exist_ok=True)
    os.makedirs(f"{BASE}/daily", exist_ok=True)

    with open(SRC_SECTOR) as f:
        sectors = json.load(f)
    with open(SRC_TICKER) as f:
        tickers = json.load(f)

    json.dump(sectors, open(f"{BASE}/latest/sectors.json","w"), indent=2)
    json.dump(tickers, open(f"{BASE}/latest/tickers.json","w"), indent=2)

    json.dump(
        {"ts": now.isoformat(), "sectors": sectors},
        open(f"{BASE}/hourly/{hour_key}.json","w"),
        indent=2
    )

    json.dump(
        {"date": day_key, "sectors": sectors},
        open(f"{BASE}/daily/{day_key}.json","w"),
        indent=2
    )

if __name__ == "__main__":
    save_snapshot()
