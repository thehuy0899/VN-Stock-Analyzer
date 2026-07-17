from dataclasses import dataclass, field
from typing import List


@dataclass
class EngineResult:

    score: int

    level: str

    summary: str

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    metrics: dict = field(default_factory=dict)