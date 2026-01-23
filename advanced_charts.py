# advanced_charts.py
# ============================================
# SAFE CHART ENGINE
# مقاوم للبيانات المتسخة
# لا يكسر التقرير أبدًا
# ============================================

import plotly.graph_objects as go
import pandas as pd


class AdvancedCharts:
    """
    محرك رسومات آمن:
    - أي خطأ في رسم → يرجع None
    - لا يفترض نظافة البيانات
    """

    # -----------------------------
    # Helpers
    # -----------------------------
    def _has_columns(self, df, cols):
        return all(c in df.columns for c in cols)

    def _to_numeric(self, series):
        try:
            return pd.to_numeric(
                series.astype(str).str.extract(r"(\d+\.?\d*)")[0],
                errors="coerce"
            )
        except Exception:
            return None

    def _base_layout(self, title):
        return dict(
            title=dict(text=title, x=0.5),
            template="plotly_white",
            height=420,
            margin=dict(l=40, r=40, t=60, b=40)
        )

    # =============================
    # الفصل 1
    # =============================
    def chapter_1_price_distribution(self, df):
        try:
            if not self._has_columns(df, ["price"]):
                return None

            price = self._to_numeric(df["price"])
            if price is None or price.dropna().empty:
                return None

            fig = go.Figure()
            fig.add_histogram(
                x=price.dropna(),
                nbinsx=20,
                marker_color="#7a0000"
            )
            fig.update_layout(self._base_layout("توزيع الأسعار"))
            return fig
        except Exception:
            return None

    def chapter_1_price_vs_area(self, df):
        try:
            if not self._has_columns(df, ["price", "area"]):
                return None

            price = self._to_numeric(df["price"])
            area = self._to_numeric(df["area"])
            mask = price.notna() & area.notna()

            if mask.sum() < 5:
                return None

            fig = go.Figure()
            fig.add_scatter(
                x=area[mask],
                y=price[mask],
                mode="markers",
                marker=dict(
                    color="#9c1c1c",
                    size=8,
                    opacity=0.6
                )
            )
            fig.update_layout(self._base_layout("العلاقة بين السعر والمساحة"))
            return fig
        except Exception:
            return None

    # =============================
    # الفصل 2
    # =============================
    def chapter_2_price_trend(self, df):
        try:
            if not self._has_columns(df, ["price", "date"]):
                return None

            price = self._to_numeric(df["price"])
            date = pd.to_datetime(df["date"], errors="coerce")

            mask = price.notna() & date.notna()
            if mask.sum() < 5:
                return None

            fig = go.Figure()
            fig.add_scatter(
                x=date[mask],
                y=price[mask],
                mode="lines",
                line=dict(color="#7a0000", width=2)
            )
            fig.update_layout(self._base_layout("تطور الأسعار مع الزمن"))
            return fig
        except Exception:
            return None

    # =============================
    # الفصل 3
    # =============================
    def chapter_3_summary_table(self, df):
        try:
            if not self._has_columns(df, ["price", "area"]):
                return None

            price = self._to_numeric(df["price"])
            area = self._to_numeric(df["area"])

            table_df = pd.DataFrame({
                "المساحة": area,
                "السعر": price
            }).dropna().head(8)

            if table_df.empty:
                return None

            fig = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=list(table_df.columns),
                            fill_color="#7a0000",
                            font=dict(color="white"),
                            align="center"
                        ),
                        cells=dict(
                            values=[table_df[c] for c in table_df.columns],
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

    # =============================
    # ENGINE
    # =============================
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
