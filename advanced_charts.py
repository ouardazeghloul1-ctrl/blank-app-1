# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    SAFE & STABLE CHARTS ENGINE
    3 رسومات لكل فصل
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
            margin=dict(l=50, r=50, t=80, b=60),
            title=dict(x=0.5, font=dict(size=16)),
            font=dict(size=12),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        return fig

    # =====================
    # RHYTHM CHARTS (SAFE)
    # =====================
    def rhythm_price_levels(self, df, title):
        if "price" not in df.columns:
            return None

        fig = px.bar(
            x=["أقل سعر", "متوسط", "أعلى سعر"],
            y=[df["price"].min(), df["price"].mean(), df["price"].max()],
            title=title,
            color_discrete_sequence=["#1A237E"],
        )
        fig.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False)
        return self._safe(fig, height=360)

    def rhythm_price_distribution(self, df, title):
        if "price" not in df.columns:
            return None

        fig = px.violin(
            df,
            y="price",
            box=True,
            points=False,
            title=title,
            color_discrete_sequence=["#3949AB"],
        )
        return self._safe(fig, height=360)

    # =====================
    # CHAPTER 1 – EXECUTIVE VERSION
    # =====================
    def ch1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        data = df[["price", "area"]].copy()
        data["price"] = pd.to_numeric(data["price"], errors="coerce")
        data["area"] = pd.to_numeric(data["area"], errors="coerce")
        data = data.dropna()

        if data.empty:
            return None

        fig = px.scatter(
            data,
            x="area",
            y="price",
            size="price",
            size_max=30,
            opacity=0.7,
            title="خريطة القيمة الاستثمارية — المساحة مقابل السعر",
            color_discrete_sequence=["#1A237E"],
        )

        # Zones (visual only – no math risk)
        fig.add_hrect(
            y0=data["price"].min(),
            y1=data["price"].median(),
            fillcolor="rgba(46,125,50,0.06)",
            line_width=0,
        )

        fig.add_hrect(
            y0=data["price"].median(),
            y1=data["price"].max(),
            fillcolor="rgba(251,192,45,0.05)",
            line_width=0,
        )

        fig.add_annotation(
            x=data["area"].median(),
            y=data["price"].median(),
            text="منطقة القيمة والفرص",
            showarrow=False,
            font=dict(size=12, color="#2E7D32"),
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
            x="date",
            y="price",
            title="تطور الأسعار مع الزمن",
            color_discrete_sequence=["#6A1B9A"],
        )
        return self._safe(fig, height=480)

    # =====================
    # CHAPTER 3
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample = df[["area", "price"]].head(10)

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color="#1A237E",
                        font=dict(color="white", size=12),
                        align="center",
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        align="center",
                        font=dict(size=11),
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
                self.rhythm_price_levels(df, "لمحة سريعة عن مستويات الأسعار"),
                self.rhythm_price_distribution(df, "توزيع الأسعار في السوق"),
            ]),
            "chapter_2": clean([
                self.ch2_price_trend(df),
                self.rhythm_price_levels(df, "مقارنة سريعة للأسعار"),
                self.rhythm_price_distribution(df, "تغيرات الأسعار"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_levels(df, "مستويات الأسعار في العينة"),
                self.rhythm_price_distribution(df, "تشتت الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_levels(df, "نطاقات الأسعار"),
                self.rhythm_price_distribution(df, "مرونة السوق"),
            ]),
            "chapter_5": clean([
                self.rhythm_price_levels(df, "مقارنة زمنية"),
                self.rhythm_price_distribution(df, "تذبذب الأسعار"),
            ]),
            "chapter_6": clean([
                self.rhythm_price_levels(df, "قراءة سريعة لرأس المال"),
                self.rhythm_price_distribution(df, "توزيع الاستثمار"),
            ]),
            "chapter_7": [],
            "chapter_8": [],
            "chapter_9": [],
            "chapter_10": [],
        }
