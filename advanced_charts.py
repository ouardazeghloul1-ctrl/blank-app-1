# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    FINAL – Stable & Premium Charts Engine
    توزيع واضح، إيقاع بصري ثابت، بدون كسر التقرير
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
    # CHAPTER 1 – MARKET SNAPSHOT
    # =====================
    def ch1_price_area_density(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        clean = df[["price", "area"]].dropna()
        if len(clean) < 20:
            return None

        y = clean["price"]
        q1, q2 = y.quantile(0.33), y.quantile(0.66)

        fig = go.Figure()
        fig.add_trace(go.Histogram2dContour(
            x=clean["area"],
            y=clean["price"],
            ncontours=20,
            showscale=False,
            colorscale=[
                [0.0, "#ede7f6"],
                [0.4, "#b39ddb"],
                [0.7, "#7e57c2"],
                [1.0, "#4527a0"],
            ],
            opacity=0.85,
        ))

        fig.add_shape(type="rect", x0=clean["area"].min(), x1=clean["area"].max(),
                      y0=clean["price"].min(), y1=q1,
                      fillcolor="rgba(76,175,80,0.08)", line_width=0)
        fig.add_shape(type="rect", x0=clean["area"].min(), x1=clean["area"].max(),
                      y0=q1, y1=q2,
                      fillcolor="rgba(255,193,7,0.08)", line_width=0)
        fig.add_shape(type="rect", x0=clean["area"].min(), x1=clean["area"].max(),
                      y0=q2, y1=clean["price"].max(),
                      fillcolor="rgba(244,67,54,0.08)", line_width=0)

        fig.update_layout(
            title="العلاقة بين المساحة والسعر — قراءة استثمارية",
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر"
        )
        return self._safe(fig, height=520)

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
        return self._safe(fig, height=380)

    def rhythm_price_distribution(self, df, title):
        if "price" not in df.columns:
            return None
        fig = px.violin(
            df, y="price", box=True, points=False,
            title=title,
            color_discrete_sequence=["#4a0000"]
        )
        return self._safe(fig, height=380)

    # =====================
    # CHAPTER 2 – TREND
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
    # CHAPTER 3 – DATA SAMPLE
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
    # CHAPTER 4 – STRATEGY
    # =====================
    def ch4_strategy_matrix(self, df):
        np.random.seed(42)
        fig = px.scatter(
            x=np.random.rand(40),
            y=np.random.rand(40),
            title="مصفوفة المخاطرة والعائد",
            labels={"x": "المخاطرة", "y": "العائد"},
            opacity=0.7
        )
        return self._safe(fig, height=480)

    # =====================
    # CHAPTER 5 – TIMING
    # =====================
    def ch5_monthly_avg(self, df):
        if "date" not in df.columns or "price" not in df.columns:
            return None
        tmp = df.copy()
        tmp["month"] = pd.to_datetime(tmp["date"]).dt.month
        agg = tmp.groupby("month")["price"].mean().reset_index()
        fig = px.bar(
            agg, x="month", y="price",
            title="متوسط الأسعار حسب الشهر",
            color="price",
            color_continuous_scale="RdBu_r"
        )
        return self._safe(fig, height=450)

    # =====================
    # CHAPTER 6 – CAPITAL
    # =====================
    def ch6_capital_pie(self):
        fig = px.pie(
            values=[30, 40, 20, 10],
            names=["الأمان", "الاستقرار", "النمو", "الفرص"],
            title="توزيع رأس المال المثالي",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_traces(textinfo="percent+label")
        return self._safe(fig, height=420)

    # =====================
    # ENGINE – FINAL DISTRIBUTION (A)
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
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_levels(df, "مستويات الأسعار في العينة"),
            ]),
            "chapter_4": clean([
                self.ch4_strategy_matrix(df),
                self.rhythm_price_levels(df, "نطاقات الأسعار حسب الاستراتيجية"),
            ]),
            "chapter_5": clean([
                self.ch5_monthly_avg(df),
                self.rhythm_price_distribution(df, "تذبذب الأسعار عبر الزمن"),
            ]),
            "chapter_6": clean([
                self.ch6_capital_pie(),
                self.rhythm_price_levels(df, "قراءة سريعة لرأس المال"),
            ]),
            # 7–8: خفيف جدًا
            "chapter_7": clean([
                self.ch2_price_trend(df),
            ]),
            "chapter_8": clean([
                self.ch1_price_area_density(df),
            ]),
            # 9–10: لا رسومات
            "chapter_9": [],
            "chapter_10": [],
        }
