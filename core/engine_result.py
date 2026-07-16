from dataclasses import dataclass, field
from typing import Any


@dataclass
class EngineResult:
    """
    Standard result returned by every analysis engine.
    """

    score: float
    confidence: float

    summary: str

    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    recommendation: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)