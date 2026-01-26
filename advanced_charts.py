# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    SAFE & STABLE CHARTS ENGINE
    Executive visual upgrade – بدون كسر أي شيء
    """

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return all(col in df.columns for col in cols)

    def _safe(self, fig, height=450):
        if fig is None:
            return None

        fig.update_layout(
            template="plotly_white",
            height=height,
            margin=dict(l=60, r=60, t=90, b=70),
            title=dict(x=0.5, font=dict(size=18)),
            font=dict(size=13),
            plot_bgcolor="rgba(245,247,250,0.9)",
            paper_bgcolor="white",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.04)")
        return fig

    # =====================
    # RHYTHM CHARTS
    # =====================
    def rhythm_price_levels(self, df, title):
        if "price" not in df.columns:
            return None

        values = [df["price"].min(), df["price"].mean(), df["price"].max()]

        fig = go.Figure(go.Bar(
            x=["أقل سعر", "متوسط", "أعلى سعر"],
            y=values,
            marker=dict(
                color=["#AED581", "#81C784", "#4CAF50"],
                line=dict(width=0)
            ),
            text=[f"{v:,.0f}" for v in values],
            textposition="outside"
        ))

        fig.update_layout(showlegend=False, title=title)
        return self._safe(fig, 360)

    def rhythm_price_distribution(self, df, title):
        if "price" not in df.columns:
            return None

        fig = go.Figure(go.Violin(
            y=df["price"],
            fillcolor="rgba(100,181,246,0.35)",
            line=dict(color="#1E88E5"),
            box_visible=True,
            meanline_visible=True
        ))

        fig.update_layout(title=title)
        return self._safe(fig, 380)

    # =====================
    # CHAPTER 1
    # =====================
    def ch1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        fig = px.scatter(
            df,
            x="area",
            y="price",
            opacity=0.6,
            color_discrete_sequence=["#5C6BC0"]
        )

        fig.update_traces(marker=dict(size=9))
        fig.update_layout(title="العلاقة بين المساحة والسعر")
        return self._safe(fig, 520)

    # =====================
    # CHAPTER 2 – EXECUTIVE CURVE (KEEP THIS)
    # =====================
    def ch2_price_trend(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["price"],
            mode="lines",
            line=dict(color="#8E24AA", width=4, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(142,36,170,0.15)"
        ))

        fig.update_layout(title="المنحنى السعري للسوق (اتجاه عام)")
        return self._safe(fig, 500)

    # =====================
    # CHAPTER 3 – TABLE (SAFE)
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample = df[["area", "price"]].head(10)

        fig = go.Figure(go.Table(
            header=dict(
                values=["المساحة", "السعر"],
                fill_color="#F2F2F2",
                font=dict(color="#333", size=14),
                align="center"
            ),
            cells=dict(
                values=[sample["area"], sample["price"]],
                fill_color="white",
                font=dict(color="#111", size=13),
                align="center"
            )
        ))

        fig.update_layout(title="عينة ذكية من بيانات السوق", height=440)
        return fig

    # =====================
    # CHAPTER 8 – BIG DONUT (NEW)
    # =====================
    def ch8_price_donut(self, df):
        if "price" not in df.columns:
            return None

        values = [
            df["price"].quantile(0.25),
            df["price"].quantile(0.5),
            df["price"].quantile(0.75)
        ]

        fig = go.Figure(go.Pie(
            labels=["اقتصادي", "متوسط", "مرتفع"],
            values=values,
            hole=0.55,
            marker=dict(colors=["#81C784", "#FFD54F", "#E57373"]),
            textinfo="label+percent"
        ))

        fig.update_layout(
            title="نطاقات الأسعار في السوق",
            height=520
        )
        return fig

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        if df is None or df.empty:
            return {}

        def clean(x): return [i for i in x if i is not None]

        return {
            "chapter_1": clean([
                self.ch1_price_vs_area(df),
                self.rhythm_price_levels(df, "لمحة سريعة عن الأسعار"),
                self.rhythm_price_distribution(df, "توزيع الأسعار"),
            ]),
            "chapter_2": clean([
                self.ch2_price_trend(df),
                self.rhythm_price_levels(df, "مقارنة سعرية"),
                self.rhythm_price_distribution(df, "تذبذب السوق"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_levels(df, "مستويات العينة"),
                self.rhythm_price_distribution(df, "تشتت الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_levels(df, "نطاقات السوق"),
                self.rhythm_price_distribution(df, "مرونة السوق"),
            ]),
            "chapter_5": clean([
                self.rhythm_price_levels(df, "قراءة زمنية"),
                self.rhythm_price_distribution(df, "تقلبات"),
            ]),
            "chapter_6": clean([
                self.rhythm_price_levels(df, "رأس المال"),
                self.rhythm_price_distribution(df, "توزيع الاستثمار"),
            ]),
            "chapter_7": clean([
                self.ch2_price_trend(df),
            ]),
            "chapter_8": clean([
                self.ch8_price_donut(df),
            ]),
            "chapter_9": [],
            "chapter_10": [],
        }
