import pandas as pd
import numpy_financial as npf


def process_investments(df, rate):
    """
    Process a DataFrame of cashflows and return NPV, IRR, and decision.

    Parameters:
    df (pd.DataFrame): Each row = one investment (CF0, CF1, ...)
    rate (float): Discount rate (e.g. 0.10 for 10%)

    Returns:
    pd.DataFrame: Results with NPV, IRR, Decision
    """

    results = []

    for _, row in df.iterrows():
        cashflows = row.values.astype(float)

        # Calculations
        npv = npf.npv(rate, cashflows)
        irr = npf.irr(cashflows)

        # Decision rule
        decision = "Accept" if npv > 0 else "Reject"

        results.append({
            "NPV": round(npv, 2),
            "IRR (%)": round(irr * 100, 2) if irr is not None else None,
            "Decision": decision
        })

    return pd.DataFrame(results)


# Optional CLI execution (useful for testing)
if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    rate = 0.10

    results = process_investments(df, rate)

    print("\nResults:\n")
    print(results)

    results.to_csv("results.csv", index=False)
    print("\nSaved to results.csv")