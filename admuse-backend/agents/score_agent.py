# agents/score_agent.py
import os, requests
from typing import Dict

FETCH_SCORER_URL = os.getenv("FETCH_SCORER_URL", "http://127.0.0.1:8001/score")

def score(creative: Dict) -> float:
    """
    Calls the Fetch.ai scoring microservice (HTTP) and returns a 0..1-ish score.
    Falls back to a trivial heuristic if the agent is unavailable.
    """
    payload = {
        "headline": creative.get("headline",""),
        "body": creative.get("body",""),
        "cta": creative.get("cta","")
    }
    try:
        res = requests.post(FETCH_SCORER_URL, json=payload, timeout=5)
        if res.ok:
            return float(res.json()["score"])
    except Exception:
        pass

    # Fallback: favor shorter, punchy copy
    h, b, c = payload["headline"], payload["body"], payload["cta"]
    return min(1.0, (len(h) < 60) * 0.4 + (len(b) < 160) * 0.4 + (len(c) < 20) * 0.2)

class ScoreAgent:
    def rank_variants(self, creatives):
        ranked = []
        for cr in creatives:
            cr["score"] = score(cr)
            ranked.append(cr)
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked
