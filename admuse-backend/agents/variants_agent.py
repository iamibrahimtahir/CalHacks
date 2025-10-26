from .common import Creative

class VariantsAgent:
    def create_variants(self, plan: dict):
        outs = []
        n = plan.get("num_variants", 6)
        for i in range(n):
            outs.append(Creative(
                id=f"AdMuse_{i+1}",
                headline=plan["hooks"][i % len(plan["hooks"])],
                body=f'{plan["value_props"][i % len(plan["value_props"])]}. Quick, fun, daily.',
                cta=plan["ctas"][i % len(plan["ctas"])],
                format=plan["formats"][i % len(plan["formats"])],
            ).dict())
        return outs
