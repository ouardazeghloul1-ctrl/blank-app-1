# advanced_charts.py
# ============================================
# High-End Visual Chart Engine
# Light + Dark Blue Theme
# Arabic + English Data Compatible
# ============================================

import plotly.graph_objects as go
import pandas as pd
import numpy as np


# ============================================
# COLOR THEMES
# ============================================

LIGHT_THEME = {
    "bg": "#FFFFFF",
    "card": "#FFFFFF",
    "grid": "#EDEDED",
    "text": "#1F2937",
    "muted": "#6B7280",
    "primary": "#6D28D9",
    "secondary": "#FACC15",
    "accent": "#06B6D4",
}

DARK_THEME = {
    "bg": "#0B1220",
    "card": "#111827",
    "grid": "#1F2937",
    "text": "#E5E7EB",
    "muted": "#9CA3AF",
    "primary": "#8B5CF6",
    "secondary": "#FACC15",
    "accent": "#22D3EE",
}


# ============================================
# MAIN ENGINE
# ============================================

class AdvancedCharts:

    def __init__(self, theme="light"):
        self.theme = DARK_THEME if theme == "dark" else LIGHT_THEME

    # ----------------------------------------
    # 🔑 NORMALIZE COLUMNS (الحل الحاسم)
    # ----------------------------------------
    def _normalize_df(self, df):
        df = df.copy()

        column_map = {
            "السعر": "price",
            "المساحة": "area",
            "المنطقة": "district",
        }

        for ar, en in column_map.items():
            if ar in df.columns and en not in df.columns:
                df[en] = df[ar]

        df = df.dropna(subset=["price", "area"])
        return df

    # ----------------------------------------
    def _layout(self, title):
        return dict(
            title=dict(
                text=title,
                font=dict(size=18, color=self.theme["text"]),
                x=0.02
            ),
            paper_bgcolor=self.theme["bg"],
            plot_bgcolor=self.theme["card"],
            font=dict(color=self.theme["text"]),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(showgrid=True, gridcolor=self.theme["grid"]),
            yaxis=dict(showgrid=True, gridcolor=self.theme["grid"]),
        )

    # ----------------------------------------
    def bar_prices_by_area(self, df):
        df = self._normalize_df(df)

        fig = go.Figure()
        fig.add_bar(
            x=df["area"],
            y=df["price"],
            marker_color=self.theme["primary"]
        )
        fig.update_layout(self._layout("العلاقة بين المساحة والسعر"))
        return fig

    # ----------------------------------------
    def donut_distribution_by_area(self, df):
        df = self._normalize_df(df)

        sizes = pd.cut(
            df["area"],
            bins=[0, 80, 120, 180, 1000],
            labels=["صغير", "متوسط", "كبير", "كبير جدًا"]
        ).value_counts()

        fig = go.Figure(
            data=[go.Pie(
                labels=sizes.index,
                values=sizes.values,
                hole=0.6,
                marker=dict(colors=[
                    self.theme["primary"],
                    self.theme["secondary"],
                    self.theme["accent"],
                    "#94A3B8"
                ])
            )]
        )

        fig.update_layout(
            title="توزيع العقارات حسب المساحة",
            paper_bgcolor=self.theme["bg"],
            font=dict(color=self.theme["text"])
        )
        return fig

    # ----------------------------------------
    def bubble_price_area(self, df):
        df = self._normalize_df(df)

        fig = go.Figure(
            data=[go.Scatter(
                x=df["area"],
                y=df["price"],
                mode="markers",
                marker=dict(
                    size=(df["price"] / df["price"].max()) * 40,
                    color=df["price"],
                    colorscale="Plasma",
                    opacity=0.75
                )
            )]
        )
        fig.update_layout(self._layout("فقاعات السعر مقابل المساحة"))
        return fig

    # ----------------------------------------
    def area_trend(self, df):
        df = self._normalize_df(df).sort_values("area")

        fig = go.Figure(
            data=[go.Scatter(
                x=df["area"],
                y=df["price"],
                fill="tozeroy",
                line=dict(color=self.theme["accent"])
            )]
        )
        fig.update_layout(self._layout("الاتجاه العام للأسعار"))
        return fig

    # ----------------------------------------
    def summary_table(self, df):
        df = self._normalize_df(df).head(10)

        fig = go.Figure(
            data=[go.Table(
                header=dict(
                    values=["المساحة", "السعر"],
                    fill_color=self.theme["primary"],
                    font=dict(color="white"),
                    align="center"
                ),
                cells=dict(
                    values=[df["area"], df["price"]],
                    fill_color=self.theme["card"],
                    font=dict(color=self.theme["text"]),
                    align="center"
                )
            )]
        )

        fig.update_layout(
            title="عينة من البيانات",
            paper_bgcolor=self.theme["bg"]
        )
        return fig

    # ----------------------------------------
    def generate_all_charts(self, df):
        return {
            "chapter_1": [
                self.bar_prices_by_area(df),
                self.donut_distribution_by_area(df),
            ],
            "chapter_2": [
                self.bubble_price_area(df),
            ],
            "chapter_3": [
                self.area_trend(df),
                self.summary_table(df),
            ],
        }
