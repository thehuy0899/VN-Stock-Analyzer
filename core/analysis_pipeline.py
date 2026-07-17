from core.financial_statement import FinancialStatement

from engines.piotroski_engine import analyze as piotroski
from engines.cashflow_engine import analyze as cashflow
from engines.valuation_engine import analyze as valuation


class AnalysisPipeline:

    def run(self, statement: FinancialStatement):

        return {
            "cashflow": cashflow(statement),
            "piotroski": piotroski(statement),
            "valuation": valuation(statement),
        }