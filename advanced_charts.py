# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    PREMIUM & SAFE CHARTS ENGINE
    3 رسومات لكل فصل
    Executive / Global Report Style
    """

    # =====================
    # BRAND IDENTITY
    # =====================
    COLORS = {
        "primary": "#1A237E",      # Indigo
        "secondary": "#3949AB",
        "accent": "#FF7043",       # Soft orange
        "muted": "#E8EAF6",
        "grid": "rgba(0,0,0,0.05)",
        "text": "#263238"
    }

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return all(col in df.columns for col in cols)

    def _safe_layout(self, fig, height=450):
        fig.update_layout(
            template="plotly_white",
            height=height,
            margin=dict(l=60, r=60, t=90, b=60),
            title=dict(
                x=0.5,
                font=dict(size=18, color=self.COLORS["primary"]),
            ),
            font=dict(size=13, color=self.COLORS["text"]),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor=self.COLORS["grid"],
            zeroline=False
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor=self.COLORS["grid"],
            zeroline=False
        )
        return fig

    # =====================
    # RHYTHM 1 — PRICE LEVELS (MODERN BAR)
    # =====================
    def rhythm_price_levels(self, df, title):
        if "price" not in df.columns:
            return None

        values = [
            df["price"].min(),
            df["price"].mean(),
            df["price"].max()
        ]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=["أقل سعر", "متوسط السوق", "أعلى سعر"],
                    y=values,
                    marker=dict(
                        color=[
                            self.COLORS["secondary"],
                            self.COLORS["primary"],
                            self.COLORS["accent"]
                        ],
                        line=dict(width=0),
                    ),
                    text=[f"{v:,.0f}" for v in values],
                    textposition="outside",
                )
            ]
        )

        fig.update_layout(title=title, showlegend=False)
        return self._safe_layout(fig, height=360)

    # =====================
    # RHYTHM 2 — DISTRIBUTION (SMOOTH HIST)
    # =====================
    def rhythm_price_distribution(self, df, title):
        if "price" not in df.columns:
            return None

        fig = px.histogram(
            df,
            x="price",
            nbins=20,
            opacity=0.9,
            title=title,
        )

        fig.update_traces(
            marker_color=self.COLORS["primary"]
        )

        mean_price = df["price"].mean()
        fig.add_vline(
            x=mean_price,
            line=dict(color=self.COLORS["accent"], width=3, dash="dash"),
            annotation_text="متوسط السوق",
            annotation_position="top",
        )

        return self._safe_layout(fig, height=360)

    # =====================
    # CHAPTER 1 — CORE RELATION
    # =====================
    def ch1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        fig = px.scatter(
            df,
            x="area",
            y="price",
            opacity=0.75,
            title="العلاقة بين المساحة والسعر",
        )

        fig.update_traces(
            marker=dict(
                size=9,
                color=self.COLORS["primary"],
                line=dict(width=1, color="white")
            )
        )

        return self._safe_layout(fig, height=520)

    # =====================
    # CHAPTER 2 — TREND
    # =====================
    def ch2_price_trend(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        fig = px.line(
            df.sort_values("date"),
            x="date",
            y="price",
            title="تطور الأسعار مع الزمن",
        )

        fig.update_traces(
            line=dict(color=self.COLORS["primary"], width=3)
        )

        return self._safe_layout(fig, height=480)

    # =====================
    # CHAPTER 3 — DATA SAMPLE
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample = df[["area", "price"]].head(8)

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color=self.COLORS["primary"],
                        font=dict(color="white", size=13),
                        align="center"
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        fill_color=self.COLORS["muted"],
                        align="center"
                    )
                )
            ]
        )

        fig.update_layout(
            title="عينة تمثيلية من بيانات السوق",
            height=420
        )

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
                self.ch1_price_vs_area(df),
                self.rhythm_price_levels(df, "لمحة سريعة عن مستويات الأسعار"),
                self.rhythm_price_distribution(df, "توزيع الأسعار في السوق"),
            ]),
            "chapter_2": clean([
                self.ch2_price_trend(df),
                self.rhythm_price_levels(df, "مقارنة مستويات الأسعار"),
                self.rhythm_price_distribution(df, "تذبذب الأسعار"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_levels(df, "قراءة سريعة للعينة"),
                self.rhythm_price_distribution(df, "انتشار الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_levels(df, "نطاقات السوق"),
                self.rhythm_price_distribution(df, "مرونة التسعير"),
            ]),
            "chapter_5": clean([
                self.rhythm_price_levels(df, "الاتجاه العام"),
                self.rhythm_price_distribution(df, "استقرار السوق"),
            ]),
            "chapter_6": clean([
                self.rhythm_price_levels(df, "قراءة رأس المال"),
                self.rhythm_price_distribution(df, "توزيع الاستثمار"),
            ]),
            "chapter_7": [],
            "chapter_8": [],
            "chapter_9": [],
            "chapter_10": [],
        }
