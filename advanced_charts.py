import plotly.express as px
import plotly.graph_objects as go


class AdvancedCharts:
    """
    AdvancedCharts
    ----------------
    محرك الرسومات الاستثماري المتقدم
    مصمم لدعم التقارير الاستشارية متعددة الفئات
    ومتوافق مع:
    - Streamlit
    - PDF Reports
    - Smart Package Downgrade
    """

    def __init__(self):
        pass

    # ======================================================
    # الفصل 1 – السيناريو العام
    # ======================================================

    def chapter_1_price_distribution(self, df):
        fig = px.histogram(
            df,
            x="price",
            nbins=30,
            title="توزيع الأسعار – قراءة سلوكية لا رقمية"
        )
        return fig

    def chapter_1_price_vs_area(self, df):
        fig = px.scatter(
            df,
            x="area",
            y="price",
            trendline="ols",
            title="العلاقة بين المساحة والسعر – هل القيمة منطقية؟"
        )
        return fig

    def chapter_1_future_scenarios(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            y=[1, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5],
            mode="lines",
            name="السيناريو الواقعي"
        ))
        fig.update_layout(title="السيناريو الواقعي لنمو السوق (10 سنوات)")
        return fig

    # ======================================================
    # الفصل 2 – المخاطر
    # ======================================================

    def chapter_2_price_concentration(self, df):
        fig = px.box(
            df,
            y="price",
            title="تمركز الأسعار – أين يتركّز الخطر؟"
        )
        return fig

    def chapter_2_price_volatility(self, df):
        fig = px.line(
            df,
            x="date",
            y="price",
            title="تذبذب الأسعار – الخطر غير المرئي"
        )
        return fig

    def chapter_2_overpricing_risk(self, df):
        fig = px.scatter(
            df,
            x="price",
            y="demand_index",
            title="مخاطر التسعير المبالغ فيه"
        )
        return fig

    # ======================================================
    # الفصل 3 – الفرص غير المرئية
    # ======================================================

    def chapter_3_value_map(self, df):
        fig = px.scatter(
            df,
            x="price",
            y="rental_yield",
            title="خريطة القيمة – أين تختبئ الفرص؟"
        )
        return fig

    def chapter_3_affordable_pockets(self, df):
        fig = px.scatter(
            df,
            x="location_score",
            y="price",
            title="الجيوب السعرية غير الملفتة"
        )
        return fig

    def chapter_3_size_opportunities(self, df):
        fig = px.scatter(
            df,
            x="area",
            y="rental_yield",
            title="المساحات المهملة ذات العائد المستقر"
        )
        return fig

    # ======================================================
    # الفصل 4 – الخطة
    # ======================================================

    def chapter_4_investment_allocation_logic(self, df):
        fig = px.pie(
            names=["أمان", "استقرار", "نمو", "فرص"],
            values=[30, 40, 20, 10],
            title="منطق توزيع الاستثمار"
        )
        return fig

    def chapter_4_action_matrix(self, df):
        fig = px.imshow(
            [[1, 2], [3, 4]],
            text_auto=True,
            title="مصفوفة القرار الاستثماري"
        )
        return fig

    # ======================================================
    # الفصل 5 – التوقيت
    # ======================================================

    def chapter_5_price_positioning(self, df):
        fig = px.line(
            df,
            x="date",
            y="price",
            title="تموضع السعر داخل الدورة"
        )
        return fig

    def chapter_5_entry_timing_signal(self, df):
        fig = px.scatter(
            df,
            x="date",
            y="entry_signal",
            title="إشارات الدخول الهادئة"
        )
        return fig

    # ======================================================
    # الفصل 6 – توزيع رأس المال
    # ======================================================

    def chapter_6_capital_allocation_by_risk(self, df):
        fig = px.bar(
            x=["منخفض", "متوسط", "مرتفع"],
            y=[50, 30, 20],
            title="توزيع رأس المال حسب مستوى المخاطر"
        )
        return fig

    def chapter_6_capital_balance_curve(self, df):
        fig = px.line(
            x=[1, 2, 3, 4, 5],
            y=[100, 110, 120, 130, 140],
            title="منحنى توازن رأس المال"
        )
        return fig

    # ======================================================
    # الفصل 7 – الخروج
    # ======================================================

    def chapter_7_exit_pressure_zones(self, df):
        fig = px.scatter(
            df,
            x="price",
            y="time_on_market",
            title="مناطق ضغط الخروج"
        )
        return fig

    def chapter_7_hold_vs_exit_signal(self, df):
        fig = px.bar(
            x=["احتفاظ", "خروج"],
            y=[70, 30],
            title="إشارة الاحتفاظ مقابل الخروج"
        )
        return fig

    # ======================================================
    # الفصل 8 – الإشارات المبكرة
    # ======================================================

    def chapter_8_anomaly_detection(self, df):
        fig = px.scatter(
            df,
            x="date",
            y="price",
            title="اكتشاف السلوك غير الطبيعي"
        )
        return fig

    def chapter_8_signal_intensity(self, df):
        fig = px.line(
            df,
            x="date",
            y="signal_strength",
            title="شدة الإشارات المبكرة"
        )
        return fig

    # ======================================================
    # المحرك الخفي – كما أرسلته تمامًا (منسجم مع التقرير)
    # ======================================================

    def generate_all_charts(self, df):
        """
        المحرك الخفي الكامل
        يولّد جميع الرسومات للفصول 1 → 8 فقط
        الفصل 9 و10 بدون رسومات (قرار استشاري)
        """

        charts = []

        charts += [
            # الفصل 1
            self.chapter_1_price_distribution(df),
            self.chapter_1_price_vs_area(df),
            self.chapter_1_future_scenarios(df),

            # الفصل 2
            self.chapter_2_price_concentration(df),
            self.chapter_2_price_volatility(df),
            self.chapter_2_overpricing_risk(df),

            # الفصل 3
            self.chapter_3_value_map(df),
            self.chapter_3_affordable_pockets(df),
            self.chapter_3_size_opportunities(df),

            # الفصل 4
            self.chapter_4_investment_allocation_logic(df),
            self.chapter_4_action_matrix(df),

            # الفصل 5
            self.chapter_5_price_positioning(df),
            self.chapter_5_entry_timing_signal(df),

            # الفصل 6
            self.chapter_6_capital_allocation_by_risk(df),
            self.chapter_6_capital_balance_curve(df),

            # الفصل 7
            self.chapter_7_exit_pressure_zones(df),
            self.chapter_7_hold_vs_exit_signal(df),

            # الفصل 8
            self.chapter_8_anomaly_detection(df),
            self.chapter_8_signal_intensity(df),
        ]

        return charts
