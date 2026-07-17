from vnstock import Reference


def load_company_data(symbol):
    symbol = symbol.upper().strip()

    ref = Reference()

    try:
        info = ref.company(symbol).info()

        outstanding_shares = int(
            info.iloc[0]["outstanding_shares"]
        )

    except Exception:
        info = None
        outstanding_shares = None

    print(info)
    print("Outstanding Shares:", outstanding_shares)

    return {
        "info": info,
        "outstanding_shares": outstanding_shares,
    }