import os
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore
from mapping.financial_overrides import directional_override # type: ignore

IN_PATH  = "data/processed/articles_with_tickers.json"
OUT_PATH = "data/processed/articles_with_sentiment.json"

def main():
    analyzer = SentimentIntensityAnalyzer()

    with open(IN_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    for a in articles:
        text = (a.get("title") or "").strip()
        score = analyzer.polarity_scores(text)

        base = score["compound"]
        override = directional_override(text)

        compound = max(-1.0, min(1.0, base + override))

        a["sentiment"] = score
        a["sentiment_compound"] = compound


    os.makedirs("data/processed", exist_ok=True)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    main()