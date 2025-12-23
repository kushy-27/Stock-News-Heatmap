import csv
import json
import os
import re

from mapping.sector_normalization import normalize_sector, load_canonical_sectors

IN_PATH = "data/processed/articles_with_entities.json"
OUT_PATH = "data/processed/articles_with_tickers.json"
MASTER_PATH = "mapping/company_master.csv"
CANONICAL_SECTORS_PATH = "mapping/canonical_sectors.txt"


def normalize_text(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s&.-]", " ", s) 
    s = re.sub(r"\s+", " ", s).strip()
    return s

def tokenize(s: str):
    s = normalize_text(s)
    parts = re.split(r"[\s&./-]+", s)
    return [p for p in parts if p]

GENERIC_TOKENS = {
    "ltd","limited","plc","inc","corp","co","company","group",
    "india","indian","the","and","services","service","industries",
    "holdings","holding","international","global","systems"
}

def title_mentions_company(title: str, company: str) -> bool:
    title_n = normalize_text(title)
    company_n = normalize_text(company)

    if not company_n or not title_n:
        return False

    if re.search(r"\b" + re.escape(company_n) + r"\b", title_n):
        return True

    t_tokens = set(tokenize(title_n))
    c_tokens = [tok for tok in tokenize(company_n)
                if tok not in GENERIC_TOKENS and len(tok) >= 3]

    if not c_tokens:
        return False

    hits = sum(1 for tok in c_tokens if tok in t_tokens)
    ratio = hits / len(c_tokens)

    if len(c_tokens) == 1:
        return hits == 1
    return ratio >= 0.6


def load_company_master(path: str):
    company_map = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"company_name", "ticker", "sector"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"company_master.csv must have columns: {required}")

        for row in reader:
            name = normalize_text(row.get("company_name", ""))
            ticker = (row.get("ticker") or "").strip()
            sector = (row.get("sector") or "").strip()
            if not name or not ticker or not sector:
                continue
            company_map[name] = {"ticker": ticker, "sector": sector}

    return company_map


def normalize_org(org: str) -> str:
    return normalize_text(org)


def map_article_entities(article, company_map, company_names, canonical_sectors):
    tickers = []
    sectors = set()
    matched_companies = []

    for org in article.get("org_entities", []):
        key = normalize_org(org)
        if key in company_map:
            info = company_map[key]
            tickers.append(info["ticker"])
            canon_sector = normalize_sector(info["sector"])
            if canon_sector in canonical_sectors:
                sectors.add(canon_sector)
            matched_companies.append(org)

    title = article.get("title", "")
    for name in company_names:
        if title_mentions_company(title, name):
            info = company_map[name]
            tickers.append(info["ticker"])
            canon_sector = normalize_sector(info["sector"])
            if canon_sector in canonical_sectors:
                sectors.add(canon_sector)
            matched_companies.append(name)

    seen = set()
    tickers_unique = []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            tickers_unique.append(t)

    article["tickers"] = tickers_unique
    article["sectors"] = sorted(list(sectors))
    article["matched_companies"] = list(dict.fromkeys(matched_companies))
    return article


def main():
    company_map = load_company_master(MASTER_PATH)
    company_names = list(company_map.keys())
    canonical_sectors = {normalize_sector(s) for s in load_canonical_sectors(CANONICAL_SECTORS_PATH)}

    with open(IN_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    mapped = [map_article_entities(a, company_map, company_names, canonical_sectors) for a in articles]

    os.makedirs("data/processed", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(mapped, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
