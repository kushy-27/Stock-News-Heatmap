import json
import os
import math
from datetime import datetime, timezone

IN_PATH = "data/processed/articles_with_sentiment.json"
OUT_PATH = "data/processed/articles_with_confidence.json"

def parse_ts(s: str) -> datetime:
    return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)

import math

SOURCE_PRIOR = {
    "moneycontrol.com": 0.95,
    "livemint.com": 0.93,
    "economictimes.indiatimes.com": 0.93,
    "thehindu.com": 0.92,
    "thehindubusinessline.com": 0.92,
}

def recency_conf(age_hours: float, tau: float = 48.0) -> float:
    return math.exp(-age_hours / tau)

def sent_conf(sent_abs: float, floor: float = 0.25) -> float:
    return min(1.0, sent_abs / floor)

def combine_match_scores(scores):
    # 1 - Π(1 - score_i)
    p = 1.0
    for s in scores:
        p *= (1.0 - max(0.0, min(1.0, s)))
    return 1.0 - p

def article_confidence(match_scores, source, age_hours, sentiment):
    if isinstance(match_scores, dict):
        scores = list(match_scores.values())
    else:
        scores = list(match_scores) if match_scores else []

    m = combine_match_scores(scores) if scores else 0.0
    src = SOURCE_PRIOR.get(source, 0.75)
    r = recency_conf(age_hours)
    sc = 0.5 + 0.5 * sent_conf(abs(sentiment))
    return m * src * r * sc


def main():
    with open(IN_PATH,"r",encoding="utf-8") as f:
        articles=json.load(f)
        
    for a in articles:
        sentiment = a.get("sentiment_compound", 0.0)
        source = a.get("source", "")

        pub = parse_ts(a["published"])
        fet = datetime.fromisoformat(a["fetched_at"]).astimezone(timezone.utc)

        age_hours = (fet - pub).total_seconds() / 3600.0

        match_scores = a.get("match_confidence")
        if not match_scores:
            match_scores = [0.7] * len(a.get("matched_companies", []))
        
        a["confidence"]=round(article_confidence(match_scores,source,age_hours,sentiment),4)
        
    with open(OUT_PATH,"w",encoding="utf-8") as f:
        json.dump(articles,f,indent=2)
    
if __name__ == "__main__":
    main()