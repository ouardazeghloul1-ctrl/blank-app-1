# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class AdvancedCharts:
    """
    EXECUTIVE / MODERN CHARTS ENGINE
    ✔ نفس عدد الرسومات
    ✔ نفس البنية
    ✔ قفزة نوعية بصرية فقط
    """

    # =====================
    # DESIGN SYSTEM (GLOBAL)
    # =====================
    COLORS = {
        "primary": "#1A237E",      # أزرق تنفيذي
        "accent": "#C62828",       # أحمر استثماري
        "soft": "#ECEFF1",         # خلفيات هادئة
        "success": "#2E7D32",
        "warning": "#F9A825"
    }

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
                font=dict(size=18, color=self.COLORS["primary"])
            ),
            font=dict(size=12, color="#333"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode="x unified"
        )

        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False
        )

        return fig

    # =====================
    # RHYTHM CHARTS (UPGRADED)
    # =====================
    def rhythm_price_levels(self, df, title):
        if "price" not in df.columns:
            return None

        fig = px.bar(
            x=["أقل سعر", "متوسط", "أعلى سعر"],
            y=[df["price"].min(), df["price"].mean(), df["price"].max()],
            title=title,
            color_discrete_sequence=[self.COLORS["primary"]]
        )

        fig.update_traces(
            texttemplate="%{y:,.0f}",
            textposition="outside",
            marker_line_width=0
        )

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
            color_discrete_sequence=[self.COLORS["accent"]]
        )

        fig.update_traces(
            meanline_visible=True,
            opacity=0.85
        )

        return self._safe(fig, height=360)

    # =====================
    # CHAPTER 1 – CORE VISUAL
    # =====================
    def ch1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        fig = px.scatter(
            df,
            x="area",
            y="price",
            opacity=0.65,
            title="العلاقة بين المساحة والسعر — خريطة القرار",
            color_discrete_sequence=[self.COLORS["primary"]]
        )

        # ZONE: VALUE SWEET SPOT
        fig.add_shape(
            type="rect",
            x0=df["area"].quantile(0.25),
            x1=df["area"].quantile(0.75),
            y0=df["price"].quantile(0.25),
            y1=df["price"].quantile(0.75),
            fillcolor="rgba(26,35,126,0.08)",
            line_width=0
        )

        fig.add_annotation(
            x=df["area"].median(),
            y=df["price"].median(),
            text="منطقة التوازن المثالي",
            showarrow=False,
            font=dict(size=13, color=self.COLORS["primary"])
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
            title="تطور الأسعار — قراءة زمنية هادئة",
            line_shape="spline",
            color_discrete_sequence=[self.COLORS["primary"]]
        )

        fig.update_traces(line_width=3)

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
                        fill_color=self.COLORS["soft"],
                        font=dict(color=self.COLORS["primary"], size=13),
                        align="center"
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        font=dict(size=12),
                        align="center"
                    )
                )
            ]
        )

        fig.update_layout(
            title="عينة واقعية من بيانات السوق",
            height=420,
            margin=dict(t=80, l=30, r=30, b=30)
        )

        return fig

    # =====================
    # ENGINE (UNCHANGED COUNT)
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
