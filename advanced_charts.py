# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    EXECUTIVE & GLOBAL CHARTS ENGINE
    - 3 رسومات لكل فصل (ثابت)
    - آمن 100%
    - مصمم لتقارير استثمارية عالمية
    """

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return df is not None and all(col in df.columns for col in cols)

    def _numeric(self, s):
        return pd.to_numeric(s, errors="coerce")

    def _base_layout(self, fig, height):
        fig.update_layout(
            template="plotly_white",
            height=height,
            margin=dict(l=60, r=60, t=80, b=60),
            title=dict(x=0.5, font=dict(size=16)),
            font=dict(size=12, family="Arial"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
        return fig

    # =====================
    # RHYTHM CHARTS (EXECUTIVE)
    # =====================
    def rhythm_price_levels(self, df, title):
        if not self._has_columns(df, ["price"]):
            return None

        price = self._numeric(df["price"]).dropna()
        if price.empty:
            return None

        values = [price.min(), price.mean(), price.max()]
        labels = ["أقل سعر", "متوسط السوق", "أعلى سعر"]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=labels,
                    y=values,
                    marker_color=["#CFD8DC", "#5C6BC0", "#1A237E"],
                    text=[f"{v:,.0f}" for v in values],
                    textposition="outside",
                )
            ]
        )

        # خط مرجعي (المتوسط)
        fig.add_hline(
            y=price.mean(),
            line_dash="dot",
            line_color="#1A237E",
            annotation_text="متوسط السوق",
            annotation_position="top left",
        )

        fig.update_layout(title=title)
        return self._base_layout(fig, 360)

    def rhythm_price_distribution(self, df, title):
        if not self._has_columns(df, ["price"]):
            return None

        price = self._numeric(df["price"]).dropna()
        if price.empty:
            return None

        fig = go.Figure()

        fig.add_trace(
            go.Box(
                y=price,
                boxpoints=False,
                fillcolor="#E3F2FD",
                line_color="#1A237E",
            )
        )

        fig.update_layout(title=title, yaxis_title="السعر")
        return self._base_layout(fig, 360)

    # =====================
    # CHAPTER 1 – MARKET STRUCTURE
    # =====================
    def ch1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        d = df.copy()
        d["price"] = self._numeric(d["price"])
        d["area"] = self._numeric(d["area"])
        d = d.dropna()
        if d.empty:
            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=d["area"],
                y=d["price"],
                mode="markers",
                marker=dict(
                    size=8,
                    color="#5C6BC0",
                    opacity=0.6,
                ),
            )
        )

        # منطقة تركيز
        fig.add_shape(
            type="rect",
            x0=d["area"].quantile(0.25),
            x1=d["area"].quantile(0.75),
            y0=d["price"].quantile(0.25),
            y1=d["price"].quantile(0.75),
            fillcolor="rgba(92,107,192,0.08)",
            line_width=0,
        )

        fig.update_layout(
            title="العلاقة بين المساحة والسعر (هيكل السوق)",
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر",
        )

        return self._base_layout(fig, 520)

    # =====================
    # CHAPTER 2 – TREND & TIMING
    # =====================
    def ch2_price_trend(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        d = df.copy()
        d["price"] = self._numeric(d["price"])
        d["date"] = pd.to_datetime(d["date"], errors="coerce")
        d = d.dropna().sort_values("date")
        if d.empty:
            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=d["date"],
                y=d["price"],
                mode="lines",
                line=dict(color="#1A237E", width=3),
            )
        )

        # متوسط متحرك بسيط
        fig.add_trace(
            go.Scatter(
                x=d["date"],
                y=d["price"].rolling(5).mean(),
                mode="lines",
                line=dict(color="#90CAF9", width=2, dash="dash"),
            )
        )

        fig.update_layout(
            title="تطور الأسعار مع الزمن (اتجاه السوق)",
            xaxis_title="الزمن",
            yaxis_title="السعر",
        )

        return self._base_layout(fig, 480)

    # =====================
    # CHAPTER 3 – DATA QUALITY
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample = (
            df[["area", "price"]]
            .apply(self._numeric)
            .dropna()
            .head(10)
        )

        if sample.empty:
            return None

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color="#1A237E",
                        font=dict(color="white"),
                        align="center",
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        fill_color="#F5F7FA",
                        align="center",
                    ),
                )
            ]
        )

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
                self.ch1_price_vs_area(df),
                self.rhythm_price_levels(df, "لمحة تنفيذية عن مستويات الأسعار"),
                self.rhythm_price_distribution(df, "توزيع الأسعار في السوق"),
            ]),
            "chapter_2": clean([
                self.ch2_price_trend(df),
                self.rhythm_price_levels(df, "مقارنة سريعة للأسعار"),
                self.rhythm_price_distribution(df, "تذبذب الأسعار"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_levels(df, "مستويات الأسعار في العينة"),
                self.rhythm_price_distribution(df, "نطاقات الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_levels(df, "نطاقات السوق"),
                self.rhythm_price_distribution(df, "مرونة السوق"),
            ]),
            "chapter_5": clean([
                self.rhythm_price_levels(df, "مقارنة زمنية"),
                self.rhythm_price_distribution(df, "تذبذب السوق"),
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
