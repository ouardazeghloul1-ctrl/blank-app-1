# advanced_charts.py
# ============================================
# High-End Visual Chart Engine
# Light + Dark Blue Theme
# Compatible with PDF / Streamlit / AI
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
    "primary": "#6D28D9",   # Purple
    "secondary": "#FACC15", # Yellow
    "accent": "#06B6D4",    # Cyan
}

DARK_THEME = {
    "bg": "#0B1220",        # Dark Blue
    "card": "#111827",
    "grid": "#1F2937",
    "text": "#E5E7EB",
    "muted": "#9CA3AF",
    "primary": "#8B5CF6",   # Soft Purple
    "secondary": "#FACC15", # Yellow
    "accent": "#22D3EE",    # Cyan
}


# ============================================
# MAIN ENGINE
# ============================================

class AdvancedCharts:
    """
    يولّد رسومات احترافية عالية المستوى
    ويعيد دائمًا plotly Figure (بدون كسر أي ملف)
    """

    def __init__(self, theme="light"):
        self.theme = DARK_THEME if theme == "dark" else LIGHT_THEME

    # ----------------------------------------
    # BASE LAYOUT
    # ----------------------------------------
    def _layout(self, title):
        return dict(
            title=dict(
                text=title,
                font=dict(size=18, color=self.theme["text"]),
                x=0.02,
                xanchor="left"
            ),
            paper_bgcolor=self.theme["bg"],
            plot_bgcolor=self.theme["card"],
            font=dict(color=self.theme["text"]),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(
                showgrid=True,
                gridcolor=self.theme["grid"],
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=self.theme["grid"],
                zeroline=False
            ),
        )

    # ----------------------------------------
    # 1️⃣ BAR CHART (فاخر – أعمدة)
    # ----------------------------------------
    def bar_prices_by_area(self, df):
        fig = go.Figure()

        fig.add_bar(
            x=df["area"],
            y=df["price"],
            marker_color=self.theme["primary"],
            name="السعر"
        )

        fig.update_layout(self._layout("العلاقة بين المساحة والسعر"))
        return fig

    # ----------------------------------------
    # 2️⃣ DONUT / PIE (مريح جدًا نفسيًا)
    # ----------------------------------------
    def donut_distribution_by_area(self, df):
        sizes = pd.cut(
            df["area"],
            bins=[0, 80, 120, 180, 1000],
            labels=["صغير", "متوسط", "كبير", "كبير جدًا"]
        ).value_counts()

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=sizes.index,
                    values=sizes.values,
                    hole=0.6,
                    marker=dict(colors=[
                        self.theme["primary"],
                        self.theme["secondary"],
                        self.theme["accent"],
                        "#94A3B8"
                    ])
                )
            ]
        )

        fig.update_layout(
            title="توزيع العقارات حسب المساحة",
            paper_bgcolor=self.theme["bg"],
            font=dict(color=self.theme["text"])
        )
        return fig

    # ----------------------------------------
    # 3️⃣ BUBBLE CHART (احترافي جدًا)
    # ----------------------------------------
    def bubble_price_area(self, df):
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df["area"],
                    y=df["price"],
                    mode="markers",
                    marker=dict(
                        size=df["price"] / df["price"].max() * 40,
                        color=df["price"],
                        colorscale="Plasma",
                        showscale=False,
                        opacity=0.75
                    )
                )
            ]
        )

        fig.update_layout(self._layout("فقاعات السعر مقابل المساحة"))
        return fig

    # ----------------------------------------
    # 4️⃣ AREA CHART (ريتم هادئ)
    # ----------------------------------------
    def area_trend(self, df):
        df_sorted = df.sort_values("area")

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_sorted["area"],
                    y=df_sorted["price"],
                    fill="tozeroy",
                    line=dict(color=self.theme["accent"])
                )
            ]
        )

        fig.update_layout(self._layout("الاتجاه العام للأسعار"))
        return fig

    # ----------------------------------------
    # 5️⃣ TABLE (مهم جدًا – أرقام واضحة)
    # ----------------------------------------
    def summary_table(self, df):
        table_df = df[["area", "price"]].head(10)

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color=self.theme["primary"],
                        font=dict(color="white", size=12),
                        align="center"
                    ),
                    cells=dict(
                        values=[
                            table_df["area"],
                            table_df["price"]
                        ],
                        fill_color=self.theme["card"],
                        font=dict(color=self.theme["text"]),
                        align="center"
                    )
                )
            ]
        )

        fig.update_layout(
            title="عينة من البيانات الفعلية",
            paper_bgcolor=self.theme["bg"]
        )
        return fig

    # ----------------------------------------
    # 🔗 GENERATE ALL (متوافق مع orchestrator)
    # ----------------------------------------
    def generate_all_charts(self, df):
        charts = {
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
        return charts
