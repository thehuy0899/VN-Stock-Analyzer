from vnstock import Quote

q = Quote(
    symbol="FPT",
    source="VCI",
)

df = q.history(
    start="2026-07-01",
    end="2026-07-17",
)

print(df.tail())
print()
print(df.columns.tolist())