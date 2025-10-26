# api.py
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os, uuid

from agents.director_claude import DirectorAgent
from agents.variants_agent import VariantsAgent
from agents.score_agent import ScoreAgent
from agents.compliance_agent import ComplianceAgent
from agents.packager_agent import PackagerAgent

app = FastAPI(title="AdMuse API")

class Brief(BaseModel):
    product: str
    audience: str
    goal: str
    tone: str = "playful"
    num_variants: int = 6

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate")
def generate(brief: Brief):
    # wire the pipeline
    director   = DirectorAgent()
    variants   = VariantsAgent()
    scorer     = ScoreAgent()
    compliance = ComplianceAgent()
    packager   = PackagerAgent()

    # start from the default plan then adjust for user input
    plan = director.generate_plan()
    plan["tone"] = brief.tone
    plan["num_variants"] = brief.num_variants
    # (you could also customize hooks/ctas based on brief fields)

    creatives = variants.create_variants(plan)
    ranked    = scorer.rank_variants(creatives)
    checked   = compliance.check(ranked)

    os.makedirs("export", exist_ok=True)
    out_name = f"max_creatives_{uuid.uuid4().hex[:8]}.zip"
    from os.path import join, abspath
    zip_path = packager.bundle(checked, join("export", out_name))

    return FileResponse(
        abspath(zip_path),
        media_type="application/zip",
        filename=out_name,
    )
