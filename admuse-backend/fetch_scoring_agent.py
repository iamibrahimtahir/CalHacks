# fetch_scoring_agent.py  — Fetch.ai scoring microservice (HTTP)
from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="Fetch.ai Scoring Agent")

class Item(BaseModel):
    headline: str
    body: str
    cta: str

def score_text(s: str) -> float:
    # simple novelty/readability heuristic (placeholder for a true model)
    words = re.findall(r"\w+", s.lower())
    uniq = len(set(words)) / max(1, len(words))
    length = min(len(s) / 140, 1.0)         # prefer concise
    punct = 1.0 if "!" in s or "?" in s else 0.8
    return round(0.4*uniq + 0.4*length + 0.2*punct, 3)

@app.post("/score")
def score(item: Item):
    h = score_text(item.headline)
    b = score_text(item.body)
    c = score_text(item.cta)
    final = round((0.5*h + 0.4*b + 0.1*c), 3)
    return {"score": final, "detail": {"headline": h, "body": b, "cta": c}}
