from data_loader import load_financial_data


symbol = "FPT"


data = load_financial_data(symbol)


print("INCOME STATEMENT")

print(
    data["income"].shape
)


print("\nBALANCE SHEET")

print(
    data["balance"].shape
)


print("\nCASH FLOW")

print(
    data["cash_flow"].shape
)