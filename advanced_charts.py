# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class AdvancedCharts:
    """
    STABLE VERSION – Curve + Donut + Table
    تعديل فقط على:
    - حجم الدائرة
    - ألوان الجدول
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
            margin=dict(l=60, r=60, t=80, b=60),
            title=dict(x=0.5, font=dict(size=16)),
            font=dict(size=12),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        return fig

    # =====================
    # CHAPTER 1 – CURVE (أعجبك)
    # =====================
    def ch1_price_curve(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        data = df.copy()
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data["price"] = pd.to_numeric(data["price"], errors="coerce")
        data = data.dropna().sort_values("date")

        if data.empty:
            return None

        fig = px.line(
            data,
            x="date",
            y="price",
            title="المنحنى السعري للسوق",
            line_shape="spline",
            color_discrete_sequence=["#7E57C2"],
        )

        fig.update_traces(line=dict(width=4))

        return self._safe(fig, height=500)

    # =====================
    # CHAPTER 2 – DONUT (مكبّرة)
    # =====================
    def ch2_price_donut(self, df):
        if "price" not in df.columns:
            return None

        price = pd.to_numeric(df["price"], errors="coerce").dropna()
        if price.empty:
            return None

        values = [
            price.min(),
            price.mean(),
            price.max()
        ]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["أقل سعر", "متوسط السعر", "أعلى سعر"],
                    values=values,
                    hole=0.55,  # Donut
                    textinfo="label+percent",
                    textfont=dict(size=14),
                    marker=dict(
                        colors=["#81C784", "#FFD54F", "#E57373"]
                    ),
                )
            ]
        )

        fig.update_layout(
            title="نطاق الأسعار في السوق",
        )

        # 🔴 تكبير الدائرة لتأخذ نصف الصفحة
        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 3 – TABLE (خلفية فاتحة)
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["area", "price"]):
            return None

        sample = df[["area", "price"]].head(10)

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color="#F5F5F5",   # فاتح جدًا
                        font=dict(color="#000000", size=12),
                        align="center",
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        fill_color="#FFFFFF",  # أبيض
                        font=dict(color="#111111", size=11),
                        align="center",
                    ),
                )
            ]
        )

        fig.update_layout(
            title="عينة ذكية من بيانات السوق",
            height=460,
        )

        return fig

    # =====================
    # ENGINE – ربط الرسومات
    # =====================
    def generate_all_charts(self, df):
        if df is None or df.empty:
            return {}

        def clean(lst):
            return [x for x in lst if x is not None]

        return {
            "chapter_1": clean([
                self.ch1_price_curve(df),
            ]),
            "chapter_2": clean([
                self.ch2_price_donut(df),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
            ]),
            "chapter_4": [],
            "chapter_5": [],
            "chapter_6": [],
            "chapter_7": [],
            "chapter_8": [],
            "chapter_9": [],
            "chapter_10": [],
        }
