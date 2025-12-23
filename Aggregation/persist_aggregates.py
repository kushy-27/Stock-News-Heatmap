import json
import os
from Aggregation.aggregate_sentiment_heatmap import compute_aggregates

IN_PATH = "Data/processed/articles_with_confidence.json"
OUT_SECTOR = "Data/processed/sector_sentiment_heatmap.json"
OUT_TICKER = "Data/processed/ticker_sentiment_heatmap.json"

def main():
    with open(IN_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    aggregates = compute_aggregates(articles)

    os.makedirs("Data", exist_ok=True)
    with open(OUT_SECTOR, "w", encoding="utf-8") as f:
        json.dump(aggregates["sectors"], f, indent=2)
    with open(OUT_TICKER, "w", encoding="utf-8") as f:
        json.dump(aggregates["tickers"], f, indent=2)

if __name__ == "__main__":
    main()
