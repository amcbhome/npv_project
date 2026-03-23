import pandas as pd
import numpy_financial as npf

RATE = 0.10

def evaluate_projects(file_path):
    df = pd.read_csv(file_path)

    results = []

    for _, row in df.iterrows():
        cashflows = row[1:].values  # skip project name
        npv = npf.npv(RATE, cashflows)
        irr = npf.irr(cashflows)

        decision = "Accept" if npv > 0 else "Reject"

        results.append({
            "Project": row["project"],
            "NPV": round(npv, 2),
            "IRR": round(irr * 100, 2),
            "Decision": decision
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    output = evaluate_projects("data/investments.csv")
    print(output)
