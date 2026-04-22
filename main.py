from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DB_NAME = "ml.db"

def setup_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS builds (hero TEXT, item TEXT)")
    c.execute("DELETE FROM builds")

    c.executemany("INSERT INTO builds VALUES (?, ?)", [
        ("Kagura", "Arcane Boots"),
        ("Kagura", "Lightning Truncheon"),
        ("Kagura", "Holy Crystal")
    ])

    conn.commit()
    conn.close()

class Query(BaseModel):
    text: str

@app.on_event("startup")
def start():
    setup_db()

@app.get("/")
def home():
    return {"message": "AI is running"}

@app.post("/ask")
def ask(q: Query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    text = q.text.lower()

    if "build" in text:
        hero = text.split("for")[-1].strip().title()
        c.execute("SELECT item FROM builds WHERE hero=?", (hero,))
        items = [x[0] for x in c.fetchall()]
        return {"hero": hero, "build": items}

    return {"message": "ask about builds"}
