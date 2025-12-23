import json
import os

IN_PATH = "data/processed/clean_articles.json"
OUT_PATH = "data/processed/filtered_articles.json"

MARKET_KEYWORDS = [
    "stock", "share", "equity", "market", "nifty", "sensex", "ipo",
    "qip", "earnings", "results", "valuation", "rally", "falls",
    "fii", "dii", "mutual fund", "sip", "rupee", "gmp"
]

BLACKLIST_KEYWORDS = [
    "horoscope", "astrology", "zodiac"
]

def looks_english(text: str) -> bool:
    if not text:
        return False
    non_ascii = sum(1 for ch in text if ord(ch) > 127)
    return (non_ascii / max(len(text), 1)) < 0.10


def is_market_article(title: str) -> bool:
    t = title.lower()
    if any(b in t for b in BLACKLIST_KEYWORDS):
        return False
    return any(k in t for k in MARKET_KEYWORDS)


def main():
    with open(IN_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    filtered = []
    for a in articles:
        title = a.get("title", "")
        if not looks_english(title):
            continue
        if not is_market_article(title):
            continue
        filtered.append(a)

    os.makedirs("data/processed", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
