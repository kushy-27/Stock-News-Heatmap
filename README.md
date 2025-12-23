# Stock-News-Heatmap
Indian Stock Market participants track the prevalent sentiment in various sectors through scattered news sources. This project builds a pipeline to track the sentiment across various sectors using live financial news, computes sentiment and plot a heatmap for it.

Overview

This project builds an end-to-end pipeline that:
-Fetches Indian stock market news in real time using GDELT API
-Extracts company names using NLP and maps them to sectors
-Applies finance-aware sentiment scoring with contextual overrides
-Aggregates sentiment using confidence and time-decay weighting
-Serves insights via FastAPI APIs and a visual dashboard

Data Pipeline Flow
1. Ingestion
Fetches Indian stock market news via GDELT API.

2. Preprocessing
Cleans titles, removes duplicates, filters irrelevant articles.

3. NLP Processing
Uses spaCy NER for organization extraction
Uses VADER for sentiment scoring

3. Mapping
Maps extracted companies to:
Stock tickers
Nifty sectors (via curated CSV)

4.Sentiment Enhancement
Directional financial overrides
Time-decay weighting
Confidence scoring

5. Aggregation
Sector-wise sentiment
Ticker-wise sentiment

6. Visualization & APIs
Heatmaps using Matplotlib
REST APIs via FastAPI

API Endpoints
| Endpoint                     | Description              |
| ---------------------------- | ------------------------ |
| `/heatmap/sectors`           | Sector sentiment heatmap |
| `/heatmap/tickers`           | Ticker sentiment heatmap |
| `/news/by-sector?sector=...` | Recent news for a sector |
| `/sectors/latest`            | Latest sector sentiment  |
| `/sectors/history`           | Historical snapshots     |

Run backend:
python -m uvicorn api.main:app --reload

Dashboard
Displays sector and ticker heatmaps
Clickable sectors to view relevant news
Powered by FastAPI + static HTML

Tech Stack
Backend: Python, FastAPI
NLP: spaCy, VADER Sentiment
Data Processing: NumPy, Pandas
Visualization: Matplotlib
Data Source: GDELT API
Frontend: HTML, JavaScript
