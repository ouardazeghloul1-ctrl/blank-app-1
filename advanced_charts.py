# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    Stable Charts Engine
    3 رسومات لكل فصل (1 أساسي + 2 إيقاعية)
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
            margin=dict(l=40, r=40, t=70, b=50),
            title=dict(x=0.5),
            font=dict(size=12),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        return fig

    # =====================
    # RHYTHM CHARTS
    # =====================
    def rhythm_price_levels(self, df, title):
        if "price" not in df.columns:
            return None
        fig = px.bar(
            x=["أقل سعر", "متوسط", "أعلى سعر"],
            y=[df["price"].min(), df["price"].mean(), df["price"].max()],
            title=title,
            color_discrete_sequence=["#7a0000"]
        )
        fig.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False)
        return self._safe(fig, height=360)

    def rhythm_price_distribution(self, df, title):
        if "price" not in df.columns:
            return None
        fig = px.violin(
            df, y="price", box=True, points=False,
            title=title,
            color_discrete_sequence=["#4a0000"]
        )
        return self._safe(fig, height=360)

    # =====================
    # CHAPTER 1
    # =====================
    def ch1_price_area_density(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        clean = df[["price", "area"]].dropna()
        if len(clean) < 20:
            return None

        fig = px.density_contour(
            clean,
            x="area",
            y="price",
            title="العلاقة بين المساحة والسعر",
            color_continuous_scale="Purples"
        )
        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 2
    # =====================
    def ch2_price_trend(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        fig = px.line(
            df.sort_values("date"),
            x="date", y="price",
            title="تطور الأسعار مع الزمن",
            line_shape="spline",
            color_discrete_sequence=["#9c1c1c"]
        )
        return self._safe(fig, height=480)

    # =====================
    # CHAPTER 3
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None
        sample = df[["area", "price"]].head(10)
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=["المساحة", "السعر"],
                fill_color="#7a0000",
                font=dict(color="white", size=14),
                align="center"
            ),
            cells=dict(
                values=[sample["area"], sample["price"]],
                align="center",
                font=dict(size=12)
            )
        )])
        fig.update_layout(title="عينة من بيانات السوق", height=420)
        return fig

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        if df is None or df.empty:
            return {}

        def clean(lst):
            return [x for x in lst if x is not None]

        return {
            "chapter_1": clean([
                self.ch1_price_area_density(df),
                self.rhythm_price_levels(df, "لمحة سريعة عن مستويات الأسعار"),
                self.rhythm_price_distribution(df, "توزيع الأسعار في السوق"),
            ]),
            "chapter_2": clean([
                self.ch2_price_trend(df),
                self.rhythm_price_levels(df, "مقارنة سريعة للأسعار"),
                self.rhythm_price_distribution(df, "توزيع الأسعار عبر الزمن"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_levels(df, "مستويات الأسعار في العينة"),
                self.rhythm_price_distribution(df, "تشتت الأسعار في السوق"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_levels(df, "نطاقات الأسعار حسب الاستراتيجية"),
                self.rhythm_price_distribution(df, "مرونة التسعير"),
            ]),
            "chapter_5": clean([
                self.rhythm_price_levels(df, "مقارنة موسمية للأسعار"),
                self.rhythm_price_distribution(df, "تذبذب الأسعار"),
            ]),
            "chapter_6": clean([
                self.rhythm_price_levels(df, "قراءة سريعة لرأس المال"),
                self.rhythm_price_distribution(df, "مرونة توزيع الاستثمار"),
            ]),
            "chapter_7": [],
            "chapter_8": [],
            "chapter_9": [],
            "chapter_10": [],
        }
