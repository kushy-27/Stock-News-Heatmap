import json
import spacy # type: ignore
from spacy.pipeline import EntityRuler # type: ignore
import csv
import re

nlp = spacy.load("en_core_web_sm")

IN_PATH = "data/processed/filtered_articles.json"
OUT_PATH = "data/processed/articles_with_entities.json"

with open(IN_PATH, "r", encoding="utf-8") as f:
    articles = json.load(f)


MAPPING_CSV = "mapping/company_master.csv"  # adjust path

ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = []

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

with open(MAPPING_CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = norm(row["company_name"])
        if name:
            patterns.append({"label": "ORG", "pattern": name})
        # optionally add ticker as ORG too
        t = norm(row["ticker"])
        if t:
            patterns.append({"label": "ORG", "pattern": t})

ruler.add_patterns(patterns)

ORG_STOPLIST = {
    "ipo","qip","qib","amc","fii","fiis","dii","diis","sip","mf",
    "inr","usd","eur","gbp","rupee","rupees","crore","crores","lakh","lakhs",
    "bse","nse","sebi","nasdaq","nyse","sensex","nifty",
    "shares","share","stock","stocks","equity","equities","market","markets",
    "exchange","company","companies","firm","firms","ltd","limited","inc",
    "corp","corporation","pvt","private",
    "ceo","cfo","cto","md","gm","vp","hr","it","ai","ml",
    "q1","q2","q3","q4","fy","yr","year","month","day",
    "india","indian","global","international","domestic","new","old"
}

def keep_org(org: str) -> bool:
    o = norm(org)
    if not o:
        return False
    low = o.lower()
    low = re.sub(r"[^a-z0-9&.\- ]+", "", low)  # strip weird chars
    low = re.sub(r"\s+", " ", low).strip()
    if low in ORG_STOPLIST:
        return False
    if len(low) <= 2:
        return False
    return True

def extract_orgs(text: str):
    doc = nlp(text)
    out = []
    for ent in doc.ents:
        if ent.label_ in {"ORG","PRODUCT"} and keep_org(ent.text):
            out.append(norm(ent.text))
    # preserve order, remove duplicates
    seen = set()
    final = []
    for x in out:
        k = x.lower()
        if k not in seen:
            seen.add(k)
            final.append(x)
    return final

for a in articles:
    title = a.get("title", "")
    a["org_entities"] = extract_orgs(title)


with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

