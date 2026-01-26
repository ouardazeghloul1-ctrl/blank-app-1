# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    SAFE & STABLE CHARTS ENGINE
    3 رسومات لكل فصل
    تطوير بصري Executive بدون كسر أي منطق
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
            title=dict(
                x=0.5,
                font=dict(size=16, color="#1f2a44")
            ),
            font=dict(
                size=12,
                color="#1f2a44"
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)

        return fig

    # =====================
    # RHYTHM CHARTS (EXECUTIVE VERSION)
    # =====================
    def rhythm_price_levels(self, df, title):
        """
        Executive Bar Chart
        هادئ – نظيف – مشابه لتقارير PowerPoint الاحترافية
        """
        if "price" not in df.columns:
            return None

        values = [
            df["price"].min(),
            df["price"].mean(),
            df["price"].max()
        ]

        labels = ["أقل سعر", "متوسط السعر", "أعلى سعر"]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=labels,
                y=values,
                width=0.55,
                marker=dict(
                    color=["#4f6bed", "#6c7cff", "#9aa5ff"],
                    line=dict(color="#e6e9f5", width=1),
                ),
                text=[f"{v:,.0f}" for v in values],
                textposition="outside",
                textfont=dict(size=13, color="#1f2a44"),
                hovertemplate="%{y:,.0f}<extra></extra>",
            )
        )

        # خط مرجعي خفيف للمتوسط
        fig.add_hline(
            y=df["price"].mean(),
            line_width=1,
            line_dash="dot",
            line_color="#b0b7d8",
            annotation_text="المتوسط",
            annotation_position="top right",
            annotation_font_size=11,
            annotation_font_color="#6b7280",
        )

        fig.update_layout(
            title=title,
            showlegend=False,
            bargap=0.35,
        )

        fig.update_yaxes(
            tickformat=",",
            ticksuffix=" ",
        )

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
            color_discrete_sequence=["#9aa5ff"]
        )

        return self._safe(fig, height=360)

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
            opacity=0.55,
            title="العلاقة بين المساحة والسعر",
            color_discrete_sequence=["#4f6bed"]
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
            color_discrete_sequence=["#4f6bed"]
        )

        fig.update_traces(line=dict(width=3))

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
                        fill_color="#eef1fb",
                        align="center",
                        font=dict(color="#1f2a44", size=12)
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        align="center",
                        font=dict(size=11)
                    )
                )
            ]
        )

        fig.update_layout(
            title="عينة من بيانات السوق",
            height=420,
            margin=dict(l=40, r=40, t=70, b=40)
        )

        return fig

    # =====================
    # ENGINE (UNCHANGED)
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
