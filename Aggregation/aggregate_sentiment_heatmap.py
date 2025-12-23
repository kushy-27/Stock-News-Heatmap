from collections import defaultdict
from datetime import datetime, timezone

def parse_ts(s):
    return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)

def time_decay_weight(published, fetched_at, half_life_hours=12.0):
    pub = parse_ts(published)
    fet = datetime.fromisoformat(fetched_at).astimezone(timezone.utc)
    age_hours = max(0.0, (fet - pub).total_seconds() / 3600.0)
    return 0.5 ** (age_hours / half_life_hours)

def upd(stats, key, w, c):
    stats[key]["count"] += c
    stats[key]["sum"] += w
    stats[key]["pos"] += max(0.0, w)
    stats[key]["neg"] += max(0.0, -w)

def finalize(stats):
    return {
        k: {
            "count": round(v["count"], 4),
            "sum_sentiment": round(v["sum"], 6),
            "avg_sentiment": round(v["sum"] / v["count"], 6) if v["count"] else 0.0,
            "pos_intensity": round(v["pos"], 6),
            "neg_intensity": round(v["neg"], 6),
        }
        for k, v in stats.items()
    }

def compute_aggregates(articles):
    sector_stats = defaultdict(lambda: {"count": 0.0, "sum": 0.0, "pos": 0.0, "neg": 0.0})
    ticker_stats = defaultdict(lambda: {"count": 0.0, "sum": 0.0, "pos": 0.0, "neg": 0.0})

    for a in articles:
        w = float(a.get("sentiment_compound", 0.0))
        if abs(w) < 0.015:
            s = 0.0
        elif w > 0:
            s = w ** 1.3
        else:
            s = -((-w) ** 1.3)

        decay = time_decay_weight(a["published"], a["fetched_at"])
        confidence = float(a.get("confidence", 1.0))

        sectors = list(dict.fromkeys(a.get("sectors", [])))
        tickers = list(dict.fromkeys(a.get("tickers", [])))

        for sec in sectors:
            upd(sector_stats, sec,
                (s * decay * confidence) / len(sectors),
                (decay * confidence) / len(sectors))

        for t in tickers:
            upd(ticker_stats, t,
                (s * decay * confidence) / len(tickers),
                (decay * confidence) / len(tickers))

    return {
        "sectors": finalize(sector_stats),
        "tickers": finalize(ticker_stats),
    }
