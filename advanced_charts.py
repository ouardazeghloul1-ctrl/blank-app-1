# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    PREMIUM EXECUTIVE CHARTS ENGINE
    مستوى عالمي – هادئ – انسيابي
    3 رسومات لكل فصل – بدون مخاطرة
    """

    # =====================
    # VISUAL IDENTITY
    # =====================
    COLORS = {
        "emerald": "#1B5E20",
        "mint": "#A5D6A7",
        "plum": "#6A1B9A",
        "lavender": "#E1BEE7",
        "gold": "#C9A227",
        "light_gray": "#F5F5F5",
        "text": "#333333",
    }

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return df is not None and all(col in df.columns for col in cols)

    def _numeric(self, s):
        return pd.to_numeric(s, errors="coerce")

    def _safe(self, fig, height=460):
        if fig is None:
            return None

        fig.update_layout(
            template="plotly_white",
            height=height,
            margin=dict(l=70, r=70, t=90, b=70),
            font=dict(size=13, color=self.COLORS["text"]),
            title=dict(
                x=0.5,
                font=dict(size=18, color=self.COLORS["text"]),
            ),
            plot_bgcolor=self.COLORS["light_gray"],
            paper_bgcolor="white",
            hovermode="x unified",
        )

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False)

        return fig

    # =====================
    # RHYTHM 1 – DONUT INSIGHT
    # =====================
    def rhythm_price_donut(self, df, title):
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if p.empty:
            return None

        values = [
            p.quantile(0.25),
            p.quantile(0.5) - p.quantile(0.25),
            p.max() - p.quantile(0.5),
        ]

        fig = go.Figure(
            data=[
                go.Pie(
                    values=values,
                    hole=0.65,
                    marker=dict(
                        colors=[
                            self.COLORS["mint"],
                            self.COLORS["lavender"],
                            self.COLORS["gold"],
                        ]
                    ),
                    textinfo="none",
                )
            ]
        )

        fig.add_annotation(
            text=f"<b>{p.mean():,.0f}</b><br>متوسط السعر",
            x=0.5,
            y=0.5,
            font=dict(size=16),
            showarrow=False,
        )

        fig.update_layout(title=title)
        return self._safe(fig, height=360)

    # =====================
    # RHYTHM 2 – SOFT DISTRIBUTION
    # =====================
    def rhythm_price_curve(self, df, title):
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 10:
            return None

        hist_y, hist_x = np.histogram(p, bins=30, density=True)
        hist_x = (hist_x[:-1] + hist_x[1:]) / 2

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hist_x,
                y=hist_y,
                mode="lines",
                line=dict(color=self.COLORS["plum"], width=3),
                fill="tozeroy",
                fillcolor="rgba(106,27,154,0.25)",
            )
        )

        fig.add_vline(
            x=p.mean(),
            line=dict(color=self.COLORS["gold"], width=2, dash="dot"),
            annotation_text="متوسط السوق",
            annotation_position="top",
        )

        fig.update_layout(title=title)
        return self._safe(fig, height=360)

    # =====================
    # CHAPTER 1 – MARKET RELATION
    # =====================
    def ch1_price_vs_area_flow(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        df = df.copy()
        df["price"] = self._numeric(df["price"])
        df["area"] = self._numeric(df["area"])
        df = df.dropna()

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["area"],
                y=df["price"],
                mode="markers",
                marker=dict(
                    size=10,
                    color=self.COLORS["emerald"],
                    opacity=0.45,
                ),
            )
        )

        fig.update_layout(
            title="العلاقة الانسيابية بين المساحة والسعر",
            xaxis_title="المساحة",
            yaxis_title="السعر",
        )

        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 2 – TIME FLOW
    # =====================
    def ch2_price_stream(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        df = df.sort_values("date")
        df["price"] = self._numeric(df["price"])

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["price"],
                mode="lines",
                line=dict(color=self.COLORS["emerald"], width=3),
                fill="tozeroy",
                fillcolor="rgba(27,94,32,0.18)",
            )
        )

        fig.update_layout(
            title="تدفق الأسعار عبر الزمن",
            xaxis_title="الزمن",
            yaxis_title="السعر",
        )

        return self._safe(fig, height=480)

    # =====================
    # CHAPTER 3 – SAMPLE TABLE
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
                        fill_color=self.COLORS["light_gray"],
                        align="center",
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        align="center",
                    ),
                )
            ]
        )

        fig.update_layout(title="عينة ذكية من بيانات السوق", height=420)
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
                self.ch1_price_vs_area_flow(df),
                self.rhythm_price_donut(df, "قراءة سريعة للسوق"),
                self.rhythm_price_curve(df, "توزيع الأسعار بانسيابية"),
            ]),
            "chapter_2": clean([
                self.ch2_price_stream(df),
                self.rhythm_price_donut(df, "مستويات الأسعار"),
                self.rhythm_price_curve(df, "زخم السوق"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_donut(df, "نطاق العينة"),
                self.rhythm_price_curve(df, "تشتت الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_donut(df, "نطاقات السوق"),
                self.rhythm_price_curve(df, "مرونة السوق"),
            ]),
            "chapter_5": clean([
                self.rhythm_price_donut(df, "مقارنة زمنية"),
                self.rhythm_price_curve(df, "ديناميكية الأسعار"),
            ]),
            "chapter_6": clean([
                self.rhythm_price_donut(df, "رأس المال"),
                self.rhythm_price_curve(df, "توزيع الاستثمار"),
            ]),
            "chapter_7": [],
            "chapter_8": [],
            "chapter_9": [],
            "chapter_10": [],
        }
