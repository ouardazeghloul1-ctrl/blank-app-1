import plotly.express as px
import plotly.graph_objects as go


class AdvancedCharts:
    """
    AdvancedCharts
    ----------------
    محرك الرسومات الاستثماري المتقدم مع تحسينات جمالية احترافية
    """

    # ===================== SAFETY & BEAUTIFICATION =====================

    def _has_columns(self, df, cols):
        return all(col in df.columns for col in cols)

    def _beautify(self, fig):
        """تحسين مظهر الرسومات لجعلها احترافية واستشارية"""
        if fig is None:
            return None
            
        fig.update_layout(
            template="plotly_white",
            width=900,
            height=520,
            margin=dict(l=40, r=40, t=80, b=50),
            title=dict(
                x=0.5,
                font=dict(size=20, family="Arial", color="#7a0000")
            ),
            font=dict(
                family="Arial",
                size=13
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # إخفاء الضجيج البصري وجعلها أنظف
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")
        
        return fig

    def _safe(self, fig):
        # ✅ حل نهائي: لا meta، لا attributes، لا مخاطرة
        return self._beautify(fig)

    # ==================================================
    # الفصل 1 – السيناريو العام
    # ==================================================

    def chapter_1_price_distribution(self, df):
        if not self._has_columns(df, ["price"]):
            return None
        try:
            fig = px.histogram(df, x="price", nbins=30,
                               title="توزيع الأسعار – قراءة سلوكية لا رقمية")
            return self._safe(fig)
        except Exception:
            return None

    def chapter_1_price_vs_area(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        try:
            # 🔹 أخذ عينة ذكية لتقليل الضجيج البصري
            sample = df.sample(
                n=min(len(df), 180),
                random_state=42
            )

            fig = px.scatter(
                sample,
                x="area",
                y="price",
                title="العلاقة بين المساحة والسعر — قراءة استثمارية هادئة",
                opacity=0.55,
            )

            # 🔹 تحسين شكل النقاط مع تدرج لوني وحجم متغير
            fig.update_traces(
                marker=dict(
                    size=sample["area"] / sample["area"].max() * 14 + 4,
                    color=sample["price"],
                    colorscale="Reds",
                    opacity=0.55,
                    showscale=False,
                    line=dict(width=0),
                )
            )

            # 🔹 تبسيط المحاور (Executive Style)
            fig.update_layout(
                xaxis_title="المساحة (م²)",
                yaxis_title="السعر",
            )

            # 🔹 إزالة أي ضجيج إضافي
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")

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
                name="السيناريو الواقعي",
                line=dict(color="#7a0000", width=3)
            ))
            fig.update_layout(title="السيناريو الواقعي لنمو السوق (10 سنوات)")
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
            fig = px.box(df, y="price",
                         title="تمركز الأسعار – أين يتركّز الخطر؟")
            fig.update_traces(marker_color="#7a0000")
            return self._safe(fig)
        except Exception:
            return None

    def chapter_2_price_volatility(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        try:
            fig = px.line(df, x="date", y="price",
                          title="تذبذب الأسعار – الخطر غير المرئي")
            fig.update_traces(line=dict(color="#d32f2f", width=2))
            return self._safe(fig)
        except Exception:
            return None

    def chapter_2_overpricing_risk(self, df):
        if not self._has_columns(df, ["price", "demand_index"]):
            return None
        try:
            fig = px.scatter(df, x="price", y="demand_index",
                             title="مخاطر التسعير المبالغ فيه")
            fig.update_traces(marker=dict(color="#ff6b6b", size=10, opacity=0.7))
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
            fig = px.scatter(df, x="price", y="rental_yield",
                             title="خريطة القيمة – أين تختبئ الفرص؟")
            fig.update_traces(marker=dict(color="#2e7d32", size=12, opacity=0.8))
            return self._safe(fig)
        except Exception:
            return None

    def chapter_3_affordable_pockets(self, df):
        if not self._has_columns(df, ["location_score", "price"]):
            return None
        try:
            fig = px.scatter(df, x="location_score", y="price",
                             title="الجيوب السعرية غير الملفتة")
            fig.update_traces(marker=dict(color="#ff9800", size=10))
            return self._safe(fig)
        except Exception:
            return None

    def chapter_3_size_opportunities(self, df):
        if not self._has_columns(df, ["area", "rental_yield"]):
            return None
        try:
            fig = px.scatter(df, x="area", y="rental_yield",
                             title="المساحات المهملة ذات العائد المستقر")
            fig.update_traces(marker=dict(color="#0097a7", size=11))
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 4 – الخطة
    # ==================================================

    def chapter_4_investment_allocation_logic(self, df):
        try:
            fig = px.pie(names=["أمان", "استقرار", "نمو", "فرص"],
                         values=[30, 40, 20, 10],
                         title="منطق توزيع الاستثمار",
                         color_discrete_sequence=["#4caf50", "#2196f3", "#ff9800", "#9c27b0"])
            return self._safe(fig)
        except Exception:
            return None

    def chapter_4_action_matrix(self, df):
        try:
            fig = px.imshow([[1, 2], [3, 4]], text_auto=True,
                            title="مصفوفة القرار الاستثماري",
                            color_continuous_scale="Blues")
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 5 – التوقيت
    # ==================================================

    def chapter_5_price_positioning(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        try:
            fig = px.line(df, x="date", y="price",
                          title="تموضع السعر داخل الدورة")
            fig.update_traces(line=dict(color="#673ab7", width=3))
            return self._safe(fig)
        except Exception:
            return None

    def chapter_5_entry_timing_signal(self, df):
        if not self._has_columns(df, ["date", "entry_signal"]):
            return None
        try:
            fig = px.scatter(df, x="date", y="entry_signal",
                             title="إشارات الدخول الهادئة")
            fig.update_traces(marker=dict(color="#e91e63", size=12, symbol="diamond"))
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 6 – رأس المال
    # ==================================================

    def chapter_6_capital_allocation_by_risk(self, df):
        try:
            fig = px.bar(x=["منخفض", "متوسط", "مرتفع"],
                         y=[50, 30, 20],
                         title="توزيع رأس المال حسب مستوى المخاطر",
                         color_discrete_sequence=["#4caf50", "#ff9800", "#f44336"])
            return self._safe(fig)
        except Exception:
            return None

    def chapter_6_capital_balance_curve(self, df):
        try:
            fig = px.line(x=[1, 2, 3, 4, 5],
                          y=[100, 110, 120, 130, 140],
                          title="منحنى توازن رأس المال")
            fig.update_traces(line=dict(color="#009688", width=3))
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 7 – الخروج
    # ==================================================

    def chapter_7_exit_pressure_zones(self, df):
        if not self._has_columns(df, ["price", "time_on_market"]):
            return None
        try:
            fig = px.scatter(df, x="price", y="time_on_market",
                             title="مناطق ضغط الخروج")
            fig.update_traces(marker=dict(color="#795548", size=11, opacity=0.7))
            return self._safe(fig)
        except Exception:
            return None

    def chapter_7_hold_vs_exit_signal(self, df):
        try:
            fig = px.bar(x=["احتفاظ", "خروج"],
                         y=[70, 30],
                         title="إشارة الاحتفاظ مقابل الخروج",
                         color_discrete_sequence=["#4caf50", "#f44336"])
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # الفصل 8 – الإشارات
    # ==================================================

    def chapter_8_anomaly_detection(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None
        try:
            fig = px.scatter(df, x="date", y="price",
                             title="اكتشاف السلوك غير الطبيعي")
            fig.update_traces(marker=dict(color="#ff5722", size=10, symbol="star"))
            return self._safe(fig)
        except Exception:
            return None

    def chapter_8_signal_intensity(self, df):
        if not self._has_columns(df, ["date", "signal_strength"]):
            return None
        try:
            fig = px.line(df, x="date", y="signal_strength",
                          title="شدة الإشارات المبكرة")
            fig.update_traces(line=dict(color="#3f51b5", width=2.5))
            return self._safe(fig)
        except Exception:
            return None

    # ==================================================
    # ENGINE مع فلترة الرسومات الفارغة
    # ==================================================

    def generate_all_charts(self, df):
        if df is None or df.empty:
            return {}

        # دالة مساعدة لتنظيف القائمة من الرسومات الفارغة
        def clean(charts):
            return [c for c in charts if c is not None]

        return {
            "chapter_1": clean([
                self.chapter_1_price_distribution(df),
                self.chapter_1_price_vs_area(df),
                self.chapter_1_future_scenarios(df),
            ]),
            "chapter_2": clean([
                self.chapter_2_price_concentration(df),
                self.chapter_2_price_volatility(df),
                self.chapter_2_overpricing_risk(df),
            ]),
            "chapter_3": clean([
                self.chapter_3_value_map(df),
                self.chapter_3_affordable_pockets(df),
                self.chapter_3_size_opportunities(df),
            ]),
            "chapter_4": clean([
                self.chapter_4_investment_allocation_logic(df),
                self.chapter_4_action_matrix(df),
            ]),
            "chapter_5": clean([
                self.chapter_5_price_positioning(df),
                self.chapter_5_entry_timing_signal(df),
            ]),
            "chapter_6": clean([
                self.chapter_6_capital_allocation_by_risk(df),
                self.chapter_6_capital_balance_curve(df),
            ]),
            "chapter_7": clean([
                self.chapter_7_exit_pressure_zones(df),
                self.chapter_7_hold_vs_exit_signal(df),
            ]),
            "chapter_8": clean([
                self.chapter_8_anomaly_detection(df),
                self.chapter_8_signal_intensity(df),
            ]),
        }
