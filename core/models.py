from dataclasses import dataclass
from typing import Optional

from core.business import Business
from core.financial import Financial


@dataclass
class Company:

    ticker: str

    name: str = ""

    sector: str = ""

    industry: str = ""

    business: Optional[Business] = None

    financial: Optional[Financial] = None