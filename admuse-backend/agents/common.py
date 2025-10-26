from pydantic import BaseModel
from typing import List
import csv, zipfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "export"
EXPORT_DIR.mkdir(exist_ok=True, parents=True)

class Plan(BaseModel):
    formats: List[str]
    value_props: List[str]
    hooks: List[str]
    ctas: List[str]
    tone: str = "playful"
    num_variants: int = 6

class Creative(BaseModel):
    id: str
    headline: str
    body: str
    cta: str
    format: str
    score: int = 0
    issues: List[str] = []

def write_manifest_and_zip(rows: List["Creative"], ab_text: str) -> str:
    out_csv = EXPORT_DIR / "manifest.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Ad Name","Format","Headline","Body","CTA","AssetPath"])
        for cr in rows:
            w.writerow([cr.id, cr.format, cr.headline, cr.body, cr.cta, f"creatives/{cr.id}.png"])

    ab_md = EXPORT_DIR / "ab_plan.md"
    ab_md.write_text(ab_text, encoding="utf-8")

    # NOTE: Do NOT create/overwrite image files here.
    # The renderer writes real PNGs into export/creatives.

    zip_path = EXPORT_DIR / "max_creatives.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(out_csv, arcname="manifest.csv")
        z.write(ab_md, arcname="ab_plan.md")
        for p in (EXPORT_DIR / "creatives").glob("*.png"):
            z.write(p, arcname=f"creatives/{p.name}")
    return str(zip_path)

def default_ab_plan() -> str:
    return (
        "# A/B Plan (AppLovin MAX)\n\n"
        "- **Goal:** Improve CTR, IR; reduce CPI\n"
        "- **Setup:** Rotate 6 variants across Banner/Interstitial/Rewarded\n"
        "- **KPIs:** Evaluate after ~5k impressions/variant\n"
        "- **Next:** Keep top 2; iterate hook/CTA on others\n"
    )
