import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import streamlit as st

def analyze_results(df):
    df = df.copy()
    df["Area(m²)"] = df["المساحة"].str.extract('(\d+)').astype(float)
    df["Price_per_m²"] = df["السعر"] / df["Area(m²)"]

    X = np.array(df["Area(m²)"]).reshape(-1, 1)
    y = np.array(df["السعر"])
    model = LinearRegression().fit(X, y)

    future_areas = np.linspace(df["Area(m²)"].min(), df["Area(m²)"].max(), 10).reshape(-1, 1)
    future_prices = model.predict(future_areas)

    prediction_df = pd.DataFrame({
        "Area(m²)": future_areas.flatten(),
        "Predicted Price ($)": future_prices.astype(int)
    })

    fig, ax = plt.subplots()
    ax.hist(df["السعر"], bins=10, color='skyblue')
    ax.set_title("توزيع أسعار العقارات" if st.session_state.lang == "ar" else "Price Distribution")
    ax.set_xlabel("السعر ($)" if st.session_state.lang == "ar" else "Price ($)")
    ax.set_ylabel("عدد العقارات" if st.session_state.lang == "ar" else "Number of Properties")
    st.pyplot(fig)

    return prediction_df
