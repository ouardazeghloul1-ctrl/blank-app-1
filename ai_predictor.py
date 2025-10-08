import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import streamlit as st

# ✅ تحليل البيانات والتنبؤ بالأسعار المستقبلية
def analyze_results(df):
    df = df.copy()
    df["Price_per_m²"] = df["Price"] / df["Area(m²)"]

    # 🔢 تدريب نموذج بسيط للتنبؤ بالأسعار المستقبلية
    X = np.array(df["Area(m²)"]).reshape(-1, 1)
    y = np.array(df["Price"])
    model = LinearRegression().fit(X, y)

    future_areas = np.linspace(50, 500, 10).reshape(-1, 1)
    future_prices = model.predict(future_areas)

    prediction_df = pd.DataFrame({
        "Area(m²)": future_areas.flatten(),
        "Predicted Price": future_prices.astype(int)
    })

    # 📊 رسم Histogram لتوزيع الأسعار
    fig, ax = plt.subplots()
    ax.hist(df["Price"], bins=10)
    ax.set_title("توزيع أسعار العقارات")
    ax.set_xlabel("السعر (بالدولار)")
    ax.set_ylabel("عدد العقارات")
    st.pyplot(fig)

    return prediction_df
