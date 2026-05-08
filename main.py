from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "data.json"

class SensorData(BaseModel):
    place: str
    area: str
    hr: float
    eda: float
    emotion: str
    note: str = ""

def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/spots")
def get_spots():
    return load_db()

@app.post("/sensor/data")
def receive_data(data: SensorData):
    db = load_db()
    record = data.dict()
    record["timestamp"] = datetime.now().isoformat()
    db.append(record)
    save_db(db)
    return {"status": "ok", "record": record}

@app.get("/stats")
def get_stats():
    db = load_db()
    total = len(db)
    emotions = {}
    for r in db:
        e = r["emotion"]
        emotions[e] = emotions.get(e, 0) + 1
    return {"total": total, "emotions": emotions}