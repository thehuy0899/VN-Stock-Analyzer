from dataclasses import dataclass

from core.business import Business
from core.industry import Industry
from core.management import Management
from core.moat import Moat
from core.valuation import Valuation


@dataclass
class InvestmentData:
    financial: dict
    business: Business
    industry: Industry
    moat: Moat
    management: Management
    valuation: Valuation