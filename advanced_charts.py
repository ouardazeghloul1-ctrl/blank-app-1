import plotly.express as px
import plotly.graph_objects as go


class AdvancedCharts:
    """
    AdvancedCharts
    ----------------
    محرك الرسومات الاستثماري المتقدم
    Contract صريح مع:
    - report_content_builder
    - report_orchestrator
    """

    # ===================== SAFETY =====================

    def _has_columns(self, df, cols):
        return all(col in df.columns for col in cols)

    def _safe(self, fig, chart_key):
        fig.meta = {"chart_key": chart_key}
        return fig

    # ==================================================
    # الفصل 1 – السيناريو العام
    # ==================================================

    def chapter_1_price_distribution(self, df):
        if not self._has_columns(df, ["price"]):
            return None
        fig = px.histogram(df, x="price", nbins=30,
                           title="توزيع الأسعار – قراءة سلوكية لا رقمية")
        return self._safe(fig, "chapter_1_price_distribution")

    def chapter_1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None
        fig = px.scatter(df, x="area", y="price", trendline="ols",
                         title="العلاقة بين المساحة والسعر")
        return self._safe(fig, "chapter_1_price_vs_area")

    def chapter_1_future_scenarios(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, 11)),
            y=[1, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5],
            mode="lines",
            name="السيناريو الواقعي"
        ))
        fig.update_layout(title="السيناريو الواقعي لنمو السوق (10 سنوات)")
        return self._safe(fig, "chapter_1_future_scenarios")

    # ==================================================
    # الفصل 2 – المخاطر
    # ==================================================

    def chapter_2_price_concentration(self, df):
        if not self._has_columns(df, ["price"]):
            return None
        fig = px.box(df, y="price",
                     title="تمركز الأسعار – أين يتركّز الخطر؟")
        return self._safe(fig, "chapter_2_price_concentration")

    def chapter_2_price_volatility(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        fig = px.line(df, x="date", y="price",
                      title="تذبذب الأسعار – الخطر غير المرئي")
        return self._safe(fig, "chapter_2_price_volatility")

    def chapter_2_overpricing_risk(self, df):
        if not self._has_columns(df, ["price", "demand_index"]):
            return None
        fig = px.scatter(df, x="price", y="demand_index",
                         title="مخاطر التسعير المبالغ فيه")
        return self._safe(fig, "chapter_2_overpricing_risk")

    # ==================================================
    # الفصل 3 – الفرص
    # ==================================================

    def chapter_3_value_map(self, df):
        if not self._has_columns(df, ["price", "rental_yield"]):
            return None
        fig = px.scatter(df, x="price", y="rental_yield",
                         title="خريطة القيمة – أين تختبئ الفرص؟")
        return self._safe(fig, "chapter_3_value_map")

    def chapter_3_affordable_pockets(self, df):
        if not self._has_columns(df, ["location_score", "price"]):
            return None
        fig = px.scatter(df, x="location_score", y="price",
                         title="الجيوب السعرية غير الملفتة")
        return self._safe(fig, "chapter_3_affordable_pockets")

    def chapter_3_size_opportunities(self, df):
        if not self._has_columns(df, ["area", "rental_yield"]):
            return None
        fig = px.scatter(df, x="area", y="rental_yield",
                         title="المساحات المهملة ذات العائد المستقر")
        return self._safe(fig, "chapter_3_size_opportunities")

    # ==================================================
    # الفصل 4 – الخطة
    # ==================================================

    def chapter_4_investment_allocation_logic(self, df):
        fig = px.pie(names=["أمان", "استقرار", "نمو", "فرص"],
                     values=[30, 40, 20, 10],
                     title="منطق توزيع الاستثمار")
        return self._safe(fig, "chapter_4_investment_allocation_logic")

    def chapter_4_action_matrix(self, df):
        fig = px.imshow([[1, 2], [3, 4]], text_auto=True,
                        title="مصفوفة القرار الاستثماري")
        return self._safe(fig, "chapter_4_action_matrix")

    # ==================================================
    # الفصل 5 – التوقيت
    # ==================================================

    def chapter_5_price_positioning(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        fig = px.line(df, x="date", y="price",
                      title="تموضع السعر داخل الدورة")
        return self._safe(fig, "chapter_5_price_positioning")

    def chapter_5_entry_timing_signal(self, df):
        if not self._has_columns(df, ["date", "entry_signal"]):
            return None
        fig = px.scatter(df, x="date", y="entry_signal",
                         title="إشارات الدخول الهادئة")
        return self._safe(fig, "chapter_5_entry_timing_signal")

    # ==================================================
    # الفصل 6 – رأس المال
    # ==================================================

    def chapter_6_capital_allocation_by_risk(self, df):
        fig = px.bar(x=["منخفض", "متوسط", "مرتفع"],
                     y=[50, 30, 20],
                     title="توزيع رأس المال حسب مستوى المخاطر")
        return self._safe(fig, "chapter_6_capital_allocation_by_risk")

    def chapter_6_capital_balance_curve(self, df):
        fig = px.line(x=[1, 2, 3, 4, 5],
                      y=[100, 110, 120, 130, 140],
                      title="منحنى توازن رأس المال")
        return self._safe(fig, "chapter_6_capital_balance_curve")

    # ==================================================
    # الفصل 7 – الخروج
    # ==================================================

    def chapter_7_exit_pressure_zones(self, df):
        if not self._has_columns(df, ["price", "time_on_market"]):
            return None
        fig = px.scatter(df, x="price", y="time_on_market",
                         title="مناطق ضغط الخروج")
        return self._safe(fig, "chapter_7_exit_pressure_zones")

    def chapter_7_hold_vs_exit_signal(self, df):
        fig = px.bar(x=["احتفاظ", "خروج"],
                     y=[70, 30],
                     title="إشارة الاحتفاظ مقابل الخروج")
        return self._safe(fig, "chapter_7_hold_vs_exit_signal")

    # ==================================================
    # الفصل 8 – الإشارات
    # ==================================================

    def chapter_8_anomaly_detection(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        fig = px.scatter(df, x="date", y="price",
                         title="اكتشاف السلوك غير الطبيعي")
        return self._safe(fig, "chapter_8_anomaly_detection")

    def chapter_8_signal_intensity(self, df):
        if not self._has_columns(df, ["date", "signal_strength"]):
            return None
        fig = px.line(df, x="date", y="signal_strength",
                      title="شدة الإشارات المبكرة")
        return self._safe(fig, "chapter_8_signal_intensity")

    # ==================================================
    # ENGINE
    # ==================================================

    def generate_all_charts(self, df):
        if df is None:
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
            "chapter_5": [
                self.chapter_5_price_positioning(df),
                self.chapter_5_entry_timing_signal(df),
            ],
            "chapter_6": [
                self.chapter_6_capital_allocation_by_risk(df),
                self.chapter_6_capital_balance_curve(df),
            ],
            "chapter_7": [
                self.chapter_7_exit_pressure_zones(df),
                self.chapter_7_hold_vs_exit_signal(df),
            ],
            "chapter_8": [
                self.chapter_8_anomaly_detection(df),
                self.chapter_8_signal_intensity(df),
            ],
        }
