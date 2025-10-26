from agents.director_claude import DirectorAgent
from agents.variants_agent import VariantsAgent
from agents.score_agent import ScoreAgent
from agents.compliance_agent import ComplianceAgent
from agents.packager_agent import PackagerAgent
import os

if __name__ == "__main__":
    print("🚀 Launching AdMuse creative pipeline...")

    director   = DirectorAgent()
    variants   = VariantsAgent()
    scorer     = ScoreAgent()
    compliance = ComplianceAgent()
    packager   = PackagerAgent()

    plan = director.generate_plan()
    print(f"Plan: formats={plan['formats']}, hooks={plan['hooks']}, ctas={plan['ctas']}")

    creatives = variants.create_variants(plan)
    ranked    = scorer.rank_variants(creatives)

    # 👇 NEW: quick visibility into the top-scored creatives from the Fetch scorer
    print(
        "Top creatives by score:",
        [(cr.get("id", i + 1), round(cr.get("score", 0.0), 3)) for i, cr in enumerate(ranked[:3])],
        flush=True
    )

    checked   = compliance.check(ranked)

    export_zip = packager.bundle(checked, os.path.join("export", "max_creatives.zip"))
    print(f"[packager] Export ready → {os.path.abspath(export_zip)}")
