import json, os
from fastapi import APIRouter, Query # type: ignore

router = APIRouter()
BASE = "storage"

@router.get("/latest")
def latest_sectors():
    path = f"{BASE}/latest/tickers.json"
    if not os.path.exists(path):
        return {}
    return json.load(open(path))


@router.get("/history")
def sector_history(
    window: str = Query("hourly", enum=["hourly","daily"]),
    limit: int = 24
):
    folder = f"{BASE}/{window}"
    if not os.path.exists(folder):
        return []

    files = sorted(os.listdir(folder), reverse=True)[:limit]
    data = []
    for f in files:
        data.append(json.load(open(os.path.join(folder,f))))
    return data