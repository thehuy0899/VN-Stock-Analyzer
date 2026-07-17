from dataclasses import dataclass


@dataclass
class PiotroskiResult:
    score: int
    passed: list[str]
    failed: list[str]