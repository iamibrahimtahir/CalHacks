from pathlib import Path
from .common import write_manifest_and_zip, default_ab_plan
from .image_renderer import render

class PackagerAgent:
    def bundle(self, creatives, export_path: str):
        export_dir = Path("export")
        assets_dir = export_dir / "creatives"
        assets_dir.mkdir(parents=True, exist_ok=True)

        # Render real PNGs
        for cr in creatives:
            render(cr, assets_dir)

        # Write manifest + zip (no image writing here)
        zip_path = write_manifest_and_zip(
            rows=[type("Obj", (), cr) for cr in creatives],
            ab_text=default_ab_plan()
        )
        return zip_path
