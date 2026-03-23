import streamlit as st
import pandas as pd
import numpy_financial as npf

st.set_page_config(page_title="NPV & IRR Tool", layout="wide")

st.title("📊 Investment Appraisal Tool")
st.write("Batch process NPV and IRR from uploaded data")

# Upload CSV
uploaded_file = st.file_uploader("Upload investment dataset (.csv)", type="csv")

# Discount rate input
rate = st.slider("Discount Rate (%)", 0.0, 20.0, 10.0) / 100

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📂 Input Data")
    st.dataframe(df)

    results = []

    for _, row in df.iterrows():
        cashflows = row.values
        npv = npf.npv(rate, cashflows)
        irr = npf.irr(cashflows)

        decision = "Accept" if npv > 0 else "Reject"

        results.append({
            "NPV": round(npv, 2),
            "IRR": round(irr * 100, 2),
            "Decision": decision
        })

    results_df = pd.DataFrame(results)

    st.subheader("📈 Results")
    st.dataframe(results_df)

    st.download_button(
        label="Download Results CSV",
        data=results_df.to_csv(index=False),
        file_name="results.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a CSV file to begin")