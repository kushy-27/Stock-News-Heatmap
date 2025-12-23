import json
import re
from hashlib import md5

RAW_PATH = "data/raw/gdelt_articles.json"
OUT_PATH = "data/processed/clean_articles.json"

with open(RAW_PATH, "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"Loaded {len(articles)} raw articles")

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

unique = {}
for a in articles:
    url = a.get("url")
    if url and url not in unique:
        unique[url] = a

articles = list(unique.values())
print(f"After URL dedup: {len(articles)}")

seen_hashes = set()
final = []

for a in articles:
    title = clean_text(a.get("title", ""))
    h = md5(title.encode("utf-8")).hexdigest()
    if h not in seen_hashes:
        seen_hashes.add(h)
        a["clean_title"] = title
        final.append(a)

import os
os.makedirs("data/processed", exist_ok=True)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

