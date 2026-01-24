# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


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

    def chapter_1_price_vs_area_density(self, df):
        """
        Density + Highlighted Zones
        رسم غني بالمعلومة ومريح بصريًا
        """
        # حماية الأعمدة
        if not all(col in df.columns for col in ["price", "area"]):
            return None

        # تنظيف وتحويل
        clean = df[["price", "area"]].copy()
        clean["price"] = pd.to_numeric(clean["price"], errors="coerce")
        clean["area"] = pd.to_numeric(clean["area"], errors="coerce")
        clean = clean.dropna()

        if len(clean) < 20:
            return None

        x = clean["area"]
        y = clean["price"]

        # حساب حدود منطقية للـ zones
        price_q1 = y.quantile(0.33)
        price_q2 = y.quantile(0.66)

        fig = go.Figure()

        # =====================
        # Density Layer
        # =====================
        fig.add_trace(
            go.Histogram2dContour(
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
                ncontours=20,
                opacity=0.85,
            )
        )

        # =====================
        # Highlighted Zones
        # =====================
        fig.add_shape(
            type="rect",
            x0=x.min(),
            x1=x.max(),
            y0=y.min(),
            y1=price_q1,
            fillcolor="rgba(76,175,80,0.08)",  # قيمة جيدة
            line_width=0,
            layer="below",
        )

        fig.add_shape(
            type="rect",
            x0=x.min(),
            x1=x.max(),
            y0=price_q1,
            y1=price_q2,
            fillcolor="rgba(255,193,7,0.08)",  # سعر عادل
            line_width=0,
            layer="below",
        )

        fig.add_shape(
            type="rect",
            x0=x.min(),
            x1=x.max(),
            y0=price_q2,
            y1=y.max(),
            fillcolor="rgba(244,67,54,0.08)",  # مبالغة
            line_width=0,
            layer="below",
        )

        # =====================
        # Annotations (معنى)
        # =====================
        fig.add_annotation(
            x=x.median(),
            y=price_q1 * 0.95,
            text="منطقة قيمة جيدة",
            showarrow=False,
            font=dict(size=12, color="#2e7d32"),
        )

        fig.add_annotation(
            x=x.median(),
            y=(price_q1 + price_q2) / 2,
            text="سعر عادل",
            showarrow=False,
            font=dict(size=12, color="#f9a825"),
        )

        fig.add_annotation(
            x=x.median(),
            y=price_q2 * 1.05,
            text="مبالغة سعرية",
            showarrow=False,
            font=dict(size=12, color="#c62828"),
        )

        # =====================
        # Layout (راحة + فخامة)
        # =====================
        fig.update_layout(
            title="العلاقة بين المساحة والسعر — قراءة استثمارية ذكية",
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر",
            template="plotly_white",
            height=520,
            margin=dict(l=40, r=40, t=80, b=50),
            font=dict(size=12),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        # ✅ التحسين: توحيد الأسلوب البصري مع _safe
        return self._safe(fig)

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
            return self._safe(fig)  # ✅ التحسين: توحيد الأسلوب البصري مع _safe
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
                self.chapter_1_price_vs_area_density(df),  # التغيير هنا فقط!
            ]),
            "chapter_2": clean([
                self.chapter_2_price_trend(df),
            ]),
            "chapter_3": clean([
                self.chapter_3_summary_table(df),
            ]),
        }
