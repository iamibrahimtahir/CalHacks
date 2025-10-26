from .common import Plan

class DirectorAgent:
    def generate_plan(self) -> dict:
        plan = Plan(
            formats=["banner","interstitial","rewarded"],
            value_props=["Daily puzzles","Train your brain","Quick fun"],
            hooks=["Beat today's puzzle!","Train your brain fast","New levels daily"],
            ctas=["Play Free","Install Now","Try a Level"],
            tone="playful",
            num_variants=6,
        )
        return plan.dict()
