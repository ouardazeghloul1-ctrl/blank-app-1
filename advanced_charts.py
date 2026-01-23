# advanced_charts.py
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


class AdvancedCharts:
    """
    AdvancedCharts – Visual First Edition
    -------------------------------------
    محرك رسومات استثماري بصري (Dark • Gradient • Calm)
    لا يعرف الباقة
    لا يقرر الكمية
    فقط يصنع رسومات جميلة ومريحة
    """

    # ===============================
    # THEME
    # ===============================
    def _base_layout(self, title):
        return dict(
            template="plotly_dark",
            title=dict(
                text=title,
                x=0.5,
                font=dict(size=20, color="#E6D7FF")
            ),
            paper_bgcolor="#0B0E14",
            plot_bgcolor="#0B0E14",
            margin=dict(l=40, r=40, t=80, b=50),
            font=dict(
                family="Tajawal, Arial",
                size=13,
                color="#E6D7FF"
            ),
            height=420
        )

    # ===============================
    # CHART TYPES (CALM & PREMIUM)
    # ===============================

    def price_distribution_area(self, df):
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df["price"],
            nbinsx=30,
            marker=dict(
                color="rgba(168,85,247,0.55)"
            )
        ))
        fig.update_layout(**self._base_layout("توزيع الأسعار — قراءة هادئة"))
        return fig

    def price_vs_area_bubble(self, df):
        sample = df.sample(n=min(len(df), 160), random_state=42)
        fig = go.Figure(
            go.Scatter(
                x=sample["area"],
                y=sample["price"],
                mode="markers",
                marker=dict(
                    size=sample["area"] / sample["area"].max() * 18 + 6,
                    color=sample["price"],
                    colorscale=[
                        [0, "#22D3EE"],
                        [0.5, "#A855F7"],
                        [1, "#EC4899"]
                    ],
                    opacity=0.55,
                    showscale=False
                )
            )
        )
        fig.update_layout(**self._base_layout("العلاقة بين المساحة والسعر"))
        fig.update_xaxes(title="المساحة (م²)")
        fig.update_yaxes(title="السعر")
        return fig

    def future_growth_area(self):
        years = list(range(1, 11))
        values = [1, 1.08, 1.12, 1.17, 1.22, 1.28, 1.33, 1.38, 1.44, 1.5]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years,
            y=values,
            fill="tozeroy",
            line=dict(color="#A855F7", width=3)
        ))
        fig.update_layout(**self._base_layout("السيناريو الواقعي لنمو السوق (10 سنوات)"))
        return fig

    def price_concentration_box(self, df):
        fig = go.Figure(
            go.Box(
                y=df["price"],
                boxpoints=False,
                marker_color="#EC4899"
            )
        )
        fig.update_layout(**self._base_layout("تمركز الأسعار — مناطق الخطر"))
        return fig

    def volatility_area(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["price"],
            fill="tozeroy",
            line=dict(color="#22D3EE", width=2)
        ))
        fig.update_layout(**self._base_layout("تذبذب السعر عبر الزمن"))
        return fig

    def value_indicator(self, value, title):
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                gauge=dict(
                    axis=dict(range=[0, 100]),
                    bar=dict(color="#A855F7"),
                    bgcolor="#0B0E14"
                ),
                number=dict(font=dict(color="#E6D7FF")),
                title=dict(text=title)
            )
        )
        fig.update_layout(**self._base_layout(""))
        return fig

    # ===============================
    # MAIN DISPATCHER (STABLE)
    # ===============================
    def generate_all_charts(self, df):
        """
        هذه الدالة تُستدعى كما هي من report_orchestrator
        لا تغيّري اسمها
        """
        return {
            "chapter_1": [
                self.price_distribution_area(df),
                self.price_vs_area_bubble(df),
                self.future_growth_area()
            ],
            "chapter_2": [
                self.price_concentration_box(df),
                self.volatility_area(df)
            ]
        }
