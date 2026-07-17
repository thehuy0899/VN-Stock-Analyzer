from vnstock import Reference

ref = Reference()

company = ref.company("FPT")

df = company.info()

print(df.columns.tolist())
print()
print(df.T)