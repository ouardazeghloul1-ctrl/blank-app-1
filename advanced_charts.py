import plotly.express as px
import plotly.graph_objects as go


class AdvancedCharts:
    """
    AdvancedCharts
    ----------------
    محرك الرسومات الاستثماري المتقدم
    (متوافق مع Streamlit Cloud بدون statsmodels)
    """

    # ===================== SAFETY =====================

    def _has_columns(self, df, cols):
        return all(col in df.columns for col in cols)

    def _safe(self, fig):
        # ❗ لا meta، لا attributes، لا مخاطرة
        return fig

    # ==================================================
    # الفصل 1 – السيناريو العام
    # ==================================================

    def chapter_1_price_distribution(self, df):
        if not self._has_columns(df, ["price"]):
            return None
        try:
            fig = px.histogram(
                df,
                x="price",
                nbins=30,
                title="توزيع الأسعار"
            )
            return self._safe(fig)
        except Exception:
            return None

    def chapter_1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None
        try:
            # ❌ لا trendline (يتطلب statsmodels)
            fig = px.scatter(
                df,
                x="area",
                y="price",
                title="العلاقة بين المساحة والسعر"
            )
            return self._safe(fig)
        except Exception:
            return None

    def chapter_1_future_scenarios(self, df):
        try:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, 11)),
                y=[1, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5],
                mode="lines",
                name="السيناريو الواقعي"
            ))
            fig.update_layout(title="سيناريو نمو السوق (10 سنوات)")
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 2 – المخاطر
    # ==================================================

    def chapter_2_price_concentration(self, df):
        if not self._has_columns(df, ["price"]):
            return None
        try:
            fig = px.box(df, y="price", title="تمركز الأسعار")
            return self._safe(fig)
        except Exception:
            return None

    def chapter_2_price_volatility(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        try:
            fig = px.line(df, x="date", y="price", title="تذبذب الأسعار")
            return self._safe(fig)
        except Exception:
            return None

    def chapter_2_overpricing_risk(self, df):
        if not self._has_columns(df, ["price", "demand_index"]):
            return None
        try:
            fig = px.scatter(
                df,
                x="price",
                y="demand_index",
                title="مخاطر التسعير المبالغ فيه"
            )
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 3 – الفرص
    # ==================================================

    def chapter_3_value_map(self, df):
        if not self._has_columns(df, ["price", "rental_yield"]):
            return None
        try:
            fig = px.scatter(
                df,
                x="price",
                y="rental_yield",
                title="خريطة القيمة"
            )
            return self._safe(fig)
        except Exception:
            return None

    def chapter_3_affordable_pockets(self, df):
        if not self._has_columns(df, ["location_score", "price"]):
            return None
        try:
            fig = px.scatter(
                df,
                x="location_score",
                y="price",
                title="الجيوب السعرية"
            )
            return self._safe(fig)
        except Exception:
            return None

    def chapter_3_size_opportunities(self, df):
        if not self._has_columns(df, ["area", "rental_yield"]):
            return None
        try:
            fig = px.scatter(
                df,
                x="area",
                y="rental_yield",
                title="فرص المساحات"
            )
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 4 – الخطة
    # ==================================================

    def chapter_4_investment_allocation_logic(self, df):
        try:
            fig = px.pie(
                names=["أمان", "استقرار", "نمو", "فرص"],
                values=[30, 40, 20, 10],
                title="توزيع الاستثمار"
            )
            return self._safe(fig)
        except Exception:
            return None

    def chapter_4_action_matrix(self, df):
        try:
            fig = px.imshow(
                [[1, 2], [3, 4]],
                text_auto=True,
                title="مصفوفة القرار"
            )
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # ENGINE
    # ==================================================

    def generate_all_charts(self, df):
        if df is None or df.empty:
            return {}

        return {
            "chapter_1": [
                self.chapter_1_price_distribution(df),
                self.chapter_1_price_vs_area(df),
                self.chapter_1_future_scenarios(df),
            ],
            "chapter_2": [
                self.chapter_2_price_concentration(df),
                self.chapter_2_price_volatility(df),
                self.chapter_2_overpricing_risk(df),
            ],
            "chapter_3": [
                self.chapter_3_value_map(df),
                self.chapter_3_affordable_pockets(df),
                self.chapter_3_size_opportunities(df),
            ],
            "chapter_4": [
                self.chapter_4_investment_allocation_logic(df),
                self.chapter_4_action_matrix(df),
            ],
        }
