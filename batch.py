import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("data.csv")

def calculate_npv(rate, cashflows):
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cashflows))

def calculate_irr(cashflows):
    try:
        return np.irr(cashflows)
    except:
        return None

results = []

for _, row in df.iterrows():
    initial = -row["initial_investment"]
    cashflows = [
        initial,
        row["year1"],
        row["year2"],
        row["year3"],
        row["year4"],
        row["year5"]
    ]

    base_rate = row["discount_rate"]
    hurdle_rate = base_rate + 0.05  # +5%

    irr = calculate_irr(cashflows)

    decision = "Reject"
    if irr is not None and irr >= hurdle_rate:
        decision = "Accept"

    results.append({
        "investment_id": row["investment_id"],
        "discount_rate": base_rate,
        "hurdle_rate": hurdle_rate,
        "IRR": irr,
        "decision": decision
    })

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv("results.csv", index=False)

print("Batch processing complete. Results saved to results.csv")