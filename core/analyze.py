from core.analysis_pipeline import AnalysisPipeline
from core.financial_statement import FinancialStatement

statement = FinancialStatement(
    revenue=1000,
    gross_profit=400,
    operating_income=250,
    net_income=180,

    total_assets=2000,
    current_assets=800,

    total_liabilities=900,
    current_liabilities=300,
    long_term_debt=400,

    equity=1100,

    operating_cashflow=220,
    free_cashflow=180,

    shares_outstanding=100
)

pipeline = AnalysisPipeline()

result = pipeline.run(statement)

print(result)