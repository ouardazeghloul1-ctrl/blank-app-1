# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go


class AdvancedCharts:
    """
    نسخة بسيطة وآمنة
    الهدف الوحيد: الرسومات تظهر بدون كسر التقرير
    """

    def _has_columns(self, df, cols):
        return all(col in df.columns for col in cols)

    def _safe(self, fig):
        if fig is None:
            return None

        fig.update_layout(
            template="plotly_white",
            height=450,
            margin=dict(l=40, r=40, t=60, b=40),
            title=dict(x=0.5)
        )
        return fig

    # =====================
    # الفصل 1
    # =====================
    def chapter_1_price_distribution(self, df):
        if not self._has_columns(df, ["price"]):
            return None
        try:
            fig = px.histogram(
                df,
                x="price",
                nbins=25,
                title="توزيع الأسعار"
            )
            return self._safe(fig)
        except Exception:
            return None

    def chapter_1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None
        try:
            fig = px.scatter(
                df,
                x="area",
                y="price",
                title="العلاقة بين السعر والمساحة",
                opacity=0.6
            )
            return self._safe(fig)
        except Exception:
            return None

    # =====================
    # الفصل 2
    # =====================
    def chapter_2_price_trend(self, df):
        if not self._has_columns(df, ["price", "date"]):
            return None
        try:
            fig = px.line(
                df,
                x="date",
                y="price",
                title="تطور الأسعار مع الزمن"
            )
            return self._safe(fig)
        except Exception:
            return None

    # =====================
    # الفصل 3
    # =====================
    def chapter_3_summary_table(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None
        try:
            sample = df[["area", "price"]].head(10)
            fig = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=["المساحة", "السعر"],
                            fill_color="#eeeeee",
                            align="center"
                        ),
                        cells=dict(
                            values=[sample["area"], sample["price"]],
                            align="center"
                        )
                    )
                ]
            )
            fig.update_layout(
                title="عينة من البيانات",
                height=300,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            return fig
        except Exception:
            return None

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        if df is None or df.empty:
            return {}

        def clean(charts):
            return [c for c in charts if c is not None]

        return {
            "chapter_1": clean([
                self.chapter_1_price_distribution(df),
                self.chapter_1_price_vs_area(df),
            ]),
            "chapter_2": clean([
                self.chapter_2_price_trend(df),
            ]),
            "chapter_3": clean([
                self.chapter_3_summary_table(df),
            ]),
        }
