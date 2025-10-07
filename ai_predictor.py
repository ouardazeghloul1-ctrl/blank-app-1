# ai_predictor.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_absolute_error

def train_price_predictor(df_prices):
    """
    df_prices: DataFrame يحتوي عمود 'price' (فريد)
    يعيد (model, poly_transformer, metrics) أو (None, None, None) إن لم تكن البيانات كافية
    """
    if df_prices is None or df_prices.empty:
        return None, None, None

    prices = df_prices['price'].values
    n = len(prices)
    if n < 6:
        return None, None, None

    X = np.arange(n).reshape(-1, 1).astype(float)
    y = prices.astype(float)

    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    # تقييم
    y_pred = model.predict(X_poly)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)

    metrics = {"r2": float(r2), "mae": float(mae)}
    return model, poly, metrics

def predict_future_prices(model, poly, df_prices, days=14):
    """
    يعيد DataFrame بـ columns ['day','predicted_price']
    """
    if model is None or poly is None or df_prices is None or df_prices.empty:
        return pd.DataFrame()

    n = len(df_prices)
    future_idx = np.arange(n, n + days).reshape(-1, 1).astype(float)
    X_future_poly = poly.transform(future_idx)
    preds = model.predict(X_future_poly)
    preds = preds.clip(min=0)
    out = pd.DataFrame({
        "day_index": list(range(n, n + days)),
        "predicted_price": preds.astype(float)
    })
    return out
