from dataclasses import dataclass


@dataclass
class Decision:
    score: int
    recommendation: str
    confidence: float
    risks: list[str]
    opportunities: list[str]