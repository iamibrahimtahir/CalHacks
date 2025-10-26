class ComplianceAgent:
    BANNED = ["#1 ever","guaranteed","free forever"]

    def check(self, creatives):
        for cr in creatives:
            issues = []
            txt = (cr["headline"] + " " + cr["body"]).lower()
            for b in self.BANNED:
                if b.lower() in txt:
                    issues.append(f"contains banned: {b}")
            cr["issues"] = issues
        return creatives
