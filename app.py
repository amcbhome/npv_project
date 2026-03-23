import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Investment Appraisal Tool", layout="wide")

st.title("📊 Investment Appraisal Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload investment data (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # --- FIXED DISCOUNT RATE ---
    # Option 1: Use CSV rate
    use_csv_rate = st.checkbox("Use Discount Rate from CSV", value=True)

    # Option 2: Fixed rate if not using CSV
    fixed_rate = st.number_input("Fixed Discount Rate (%)", value=10.0) / 100

    # --- CALCULATE BUTTON ---
    if st.button("Calculate"):

        results = []

        for _, row in df.iterrows():

            # Choose rate
            if use_csv_rate and "Discount_Rate" in df.columns:
                r = row["Discount_Rate"]
            else:
                r = fixed_rate

            cashflows = [
                row["Year1"],
                row["Year2"],
                row["Year3"],
                row["Year4"],
                row["Year5"]
            ]

            # --- NPV ---
            npv = -row["Initial_Investment"]
            for t, cf in enumerate(cashflows, start=1):
                npv += cf / ((1 + r) ** t)

            # --- IRR ---
            try:
                irr = np.irr([-row["Initial_Investment"]] + cashflows)
            except:
                irr = None

            # --- Decision ---
            decision = "ACCEPT" if npv > 0 else "REJECT"

            results.append({
                "Investment_ID": row["Investment_ID"],
                "NPV": round(npv, 2),
                "IRR": round(irr, 4) if irr else None,
                "Decision": decision
            })

        results_df = pd.DataFrame(results)

        st.subheader("Results")
        st.dataframe(results_df)

        # --- Summary ---
        st.subheader("Summary")
        total = len(results_df)
        accepted = len(results_df[results_df["Decision"] == "ACCEPT"])
        rejected = len(results_df[results_df["Decision"] == "REJECT"])

        st.write(f"Total Investments: {total}")
        st.write(f"Accepted: {accepted}")
        st.write(f"Rejected: {rejected}")
        st.write(f"Acceptance Rate: {accepted/total:.2%}")