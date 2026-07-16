from core.decision import Decision

decision = Decision(
    score=85,
    recommendation="Buy",
    confidence=0.82,
    risks=["China Dumping"],
    opportunities=["Public Investment"],
)

print(decision)