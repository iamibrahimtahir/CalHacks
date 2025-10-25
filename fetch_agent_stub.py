# uAgents-style stub
def run_variant_job(plan: dict, n: int = 3):
    return [ { 'variant': i, 'score': round(0.5 + i*0.1, 2) } for i in range(n) ]
