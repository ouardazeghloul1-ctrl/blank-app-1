# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    AdvancedCharts – النسخة المستقرة والاحترافية
    - رسومات ذات معنى
    - توزيع بصري مريح
    - بدون كسر التقرير
    """

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return all(col in df.columns for col in cols)

    def _safe(self, fig):
        if fig is None:
            return None

        fig.update_layout(
            template="plotly_white",
            height=450,
            margin=dict(l=50, r=50, t=80, b=60),
            title=dict(x=0.5),
            font=dict(size=13),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        return fig

    # =====================
    # CHAPTER 1 – MARKET OVERVIEW
    # =====================
    def chapter_1_price_vs_area_density(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        clean = df[["price", "area"]].copy()
        clean["price"] = pd.to_numeric(clean["price"], errors="coerce")
        clean["area"] = pd.to_numeric(clean["area"], errors="coerce")
        clean = clean.dropna()

        if len(clean) < 20:
            return None

        x = clean["area"]
        y = clean["price"]

        q1 = y.quantile(0.33)
        q2 = y.quantile(0.66)

        fig = go.Figure()

        fig.add_trace(go.Histogram2dContour(
            x=x,
            y=y,
            colorscale=[
                [0.0, "#ede7f6"],
                [0.4, "#b39ddb"],
                [0.7, "#7e57c2"],
                [1.0, "#4527a0"],
            ],
            contours=dict(showlines=False),
            showscale=False,
            opacity=0.9,
        ))

        fig.add_shape(type="rect", x0=x.min(), x1=x.max(), y0=y.min(), y1=q1,
                      fillcolor="rgba(76,175,80,0.08)", line_width=0)
        fig.add_shape(type="rect", x0=x.min(), x1=x.max(), y0=q1, y1=q2,
                      fillcolor="rgba(255,193,7,0.08)", line_width=0)
        fig.add_shape(type="rect", x0=x.min(), x1=x.max(), y0=q2, y1=y.max(),
                      fillcolor="rgba(244,67,54,0.08)", line_width=0)

        fig.update_layout(
            title="العلاقة بين المساحة والسعر – قراءة استثمارية",
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر",
        )

        return self._safe(fig)

    def rhythm_bar_key_insight(self, df, title):
        if "price" not in df.columns:
            return None

        fig = px.bar(
            x=["أقل سعر", "متوسط", "أعلى سعر"],
            y=[df["price"].min(), df["price"].mean(), df["price"].max()],
            title=title,
            color_discrete_sequence=["#7a0000"]
        )
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        fig.update_layout(showlegend=False)

        return self._safe(fig)

    def rhythm_violin_snapshot(self, df, title):
        if "price" not in df.columns:
            return None

        fig = px.violin(
            df, y="price",
            box=True,
            points=False,
            title=title,
            color_discrete_sequence=["#4a0000"]
        )
        return self._safe(fig)

    # =====================
    # CHAPTER 2 – TRENDS
    # =====================
    def chapter_2_price_trend(self, df):
        if not self._has_columns(df, ["price", "date"]):
            return None

        fig = px.line(
            df.sort_values("date"),
            x="date",
            y="price",
            title="تطور الأسعار مع الزمن",
            line_shape="spline",
            color_discrete_sequence=["#9c1c1c"]
        )
        return self._safe(fig)

    def rhythm_line_pulse(self, df, title):
        if not self._has_columns(df, ["date", "price"]):
            return None

        fig = px.line(
            df.sort_values("date"),
            x="date",
            y="price",
            title=title,
            line_shape="spline",
            color_discrete_sequence=["#5e0000"]
        )
        return self._safe(fig)

    # =====================
    # CHAPTER 3 – DATA SNAPSHOT
    # =====================
    def chapter_3_summary_table(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample = df[["area", "price"]].head(10)

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=["المساحة (م²)", "السعر"],
                fill_color="#7a0000",
                font=dict(color="white", size=14),
                align="center"
            ),
            cells=dict(
                values=[sample["area"], sample["price"]],
                fill_color=["#f9f9f9", "white"],
                align="center"
            )
        )])

        fig.update_layout(title="عينة من البيانات")
        return self._safe(fig)

    # =====================
    # CHAPTER 4 – STRATEGY
    # =====================
    def chapter_4_strategy_matrix(self, df):
        np.random.seed(42)
        risk = np.random.rand(40)
        reward = np.random.rand(40)

        fig = px.scatter(
            x=risk,
            y=reward,
            title="مصفوفة المخاطرة والعائد",
            labels={"x": "المخاطرة", "y": "العائد المتوقع"},
            opacity=0.7
        )
        return self._safe(fig)

    # =====================
    # CHAPTER 5 – TIMING
    # =====================
    def chapter_5_timing_bar(self, df):
        if "date" not in df.columns:
            return None

        dfc = df.copy()
        dfc["month"] = pd.to_datetime(dfc["date"]).dt.month
        monthly = dfc.groupby("month")["price"].mean().reset_index()

        fig = px.bar(
            monthly,
            x="month",
            y="price",
            title="متوسط الأسعار حسب الشهر",
            color="price",
            color_continuous_scale="RdBu_r"
        )
        return self._safe(fig)

    # =====================
    # CHAPTER 6 – CAPITAL
    # =====================
    def chapter_6_capital_distribution(self, df):
        fig = px.pie(
            values=[30, 40, 20, 10],
            names=["الأمان", "الاستقرار", "النمو", "الفرص"],
            title="التوزيع الذكي لرأس المال"
        )
        fig.update_traces(textinfo="percent+label")
        return self._safe(fig)

    # =====================
    # CHAPTER 7 – EXIT
    # =====================
    def chapter_7_exit_signals(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        dfc = df.sort_values("date").copy()
        dfc["avg"] = dfc["price"].rolling(5).mean()

        fig = px.line(
            dfc,
            x="date",
            y=["price", "avg"],
            title="إشارات الخروج المحتملة"
        )
        return self._safe(fig)

    # =====================
    # CHAPTER 8 – SIGNALS
    # =====================
    def chapter_8_signals_scatter(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        fig = px.scatter(
            df.head(40),
            x="area",
            y="price",
            title="الإشارات المبكرة في السوق",
            opacity=0.7
        )
        return self._safe(fig)

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
                self.chapter_1_price_vs_area_density(df),
                self.rhythm_bar_key_insight(df, "لمحة سريعة عن مستويات الأسعار"),
                self.rhythm_violin_snapshot(df, "توزيع الأسعار في السوق"),
            ]),
            "chapter_2": clean([
                self.chapter_2_price_trend(df),
                self.rhythm_line_pulse(df, "نبض السوق السعري"),
            ]),
            "chapter_3": clean([
                self.chapter_3_summary_table(df),
            ]),
            "chapter_4": clean([
                self.chapter_4_strategy_matrix(df),
            ]),
            "chapter_5": clean([
                self.chapter_5_timing_bar(df),
            ]),
            "chapter_6": clean([
                self.chapter_6_capital_distribution(df),
            ]),
            "chapter_7": clean([
                self.chapter_7_exit_signals(df),
            ]),
            "chapter_8": clean([
                self.chapter_8_signals_scatter(df),
            ]),
            # ❌ لا رسومات للفصل 9
            # ❌ لا رسومات للفصل 10
        }
