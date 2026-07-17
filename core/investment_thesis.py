from dataclasses import dataclass, field

@dataclass
class InvestmentThesis:

    summary: str

    strengths: list[str] = field(default_factory=list)

    weaknesses: list[str] = field(default_factory=list)

    catalysts: list[str] = field(default_factory=list)

    risks: list[str] = field(default_factory=list)