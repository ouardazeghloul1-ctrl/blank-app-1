import plotly.express as px
import plotly.graph_objects as go

class AdvancedCharts:
    """
    AdvancedCharts v2
    Visual Decision Engine
    """

    # -----------------------------
    # UTILITIES
    # -----------------------------
    def _has(self, df, cols):
        return df is not None and all(c in df.columns for c in cols)

    def _beautify(self, fig, title):
        if fig is None:
            return None

        fig.update_layout(
            template="plotly_white",
            height=480,
            margin=dict(l=40, r=40, t=70, b=40),
            title=dict(
                text=title,
                x=0.5,
                font=dict(size=18, color="#7a0000")
            ),
            font=dict(size=12),
            showlegend=False
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")
        return fig

    # ==================================================
    # CHAPTER 1 – SCENARIO
    # ==================================================
    def chapter_1(self, df):
        charts = {}

        # HERO – Timeline / Area
        if self._has(df, ["date", "price"]):
            fig = px.area(df, x="date", y="price")
            charts["hero"] = self._beautify(
                fig, "المسار العام للسوق — قراءة هادئة"
            )

        charts["supporting"] = []

        # Distribution
        if self._has(df, ["price"]):
            fig = px.histogram(df, x="price", nbins=25)
            charts["supporting"].append(
                self._beautify(fig, "نطاق الأسعار السائد")
            )

        # Growth Curve
        if self._has(df, ["date", "growth_rate"]):
            fig = px.line(df, x="date", y="growth_rate")
            charts["supporting"].append(
                self._beautify(fig, "إيقاع النمو عبر الزمن")
            )

        return charts

    # ==================================================
    # CHAPTER 2 – RISKS
    # ==================================================
    def chapter_2(self, df):
        charts = {}

        if self._has(df, ["price"]):
            fig = px.box(df, y="price")
            charts["hero"] = self._beautify(
                fig, "تمركز الأسعار — أين يتركّز الخطر"
            )

        charts["supporting"] = []

        if self._has(df, ["date", "price"]):
            fig = px.line(df, x="date", y="price")
            charts["supporting"].append(
                self._beautify(fig, "تذبذب السعر بمرور الوقت")
            )

        if self._has(df, ["price", "demand_index"]):
            fig = px.scatter(df, x="price", y="demand_index", opacity=0.5)
            charts["supporting"].append(
                self._beautify(fig, "مخاطر التسعير المبالغ فيه")
            )

        return charts

    # ==================================================
    # CHAPTER 3 – OPPORTUNITIES
    # ==================================================
    def chapter_3(self, df):
        charts = {}

        if self._has(df, ["price", "rental_yield"]):
            fig = px.scatter(df, x="price", y="rental_yield", opacity=0.6)
            charts["hero"] = self._beautify(
                fig, "خريطة الفرص — القيمة مقابل العائد"
            )

        charts["supporting"] = []

        if self._has(df, ["location_score", "price"]):
            fig = px.scatter(df, x="location_score", y="price", opacity=0.6)
            charts["supporting"].append(
                self._beautify(fig, "الجيوب السعرية غير الملفتة")
            )

        if self._has(df, ["area", "rental_yield"]):
            fig = px.scatter(df, x="area", y="rental_yield", opacity=0.6)
            charts["supporting"].append(
                self._beautify(fig, "المساحات ذات العائد المستقر")
            )

        return charts

    # ==================================================
    # CHAPTER 4 – STRATEGY
    # ==================================================
    def chapter_4(self, df):
        charts = {}

        fig = px.pie(
            names=["أمان", "استقرار", "نمو", "فرص"],
            values=[30, 40, 20, 10]
        )
        charts["hero"] = self._beautify(
            fig, "منطق توزيع الاستثمار"
        )

        charts["supporting"] = []

        fig = px.imshow(
            [[1, 2], [3, 4]],
            text_auto=True,
            color_continuous_scale="Greys"
        )
        charts["supporting"].append(
            self._beautify(fig, "مصفوفة القرار الاستثماري")
        )

        return charts

    # ==================================================
    # CHAPTER 5 – TIMING
    # ==================================================
    def chapter_5(self, df):
        charts = {}

        if self._has(df, ["date", "price"]):
            fig = px.line(df, x="date", y="price")
            charts["hero"] = self._beautify(
                fig, "تموضع السعر داخل الدورة"
            )

        charts["supporting"] = []

        if self._has(df, ["date", "entry_signal"]):
            fig = px.scatter(df, x="date", y="entry_signal")
            charts["supporting"].append(
                self._beautify(fig, "إشارات الدخول الهادئة")
            )

        return charts

    # ==================================================
    # CHAPTER 6 – CAPITAL
    # ==================================================
    def chapter_6(self, df):
        charts = {}

        fig = px.bar(
            x=["أمان", "استقرار", "نمو", "فرص"],
            y=[30, 40, 20, 10]
        )
        charts["hero"] = self._beautify(
            fig, "طبقات توزيع رأس المال"
        )

        charts["supporting"] = []

        fig = px.line(x=[1,2,3,4,5], y=[100,110,120,130,140])
        charts["supporting"].append(
            self._beautify(fig, "منحنى توازن رأس المال")
        )

        return charts

    # ==================================================
    # CHAPTER 7 – EXIT
    # ==================================================
    def chapter_7(self, df):
        charts = {}

        if self._has(df, ["price", "time_on_market"]):
            fig = px.scatter(df, x="price", y="time_on_market", opacity=0.6)
            charts["hero"] = self._beautify(
                fig, "مناطق ضغط الخروج"
            )

        charts["supporting"] = []

        fig = px.bar(x=["احتفاظ", "خروج"], y=[70, 30])
        charts["supporting"].append(
            self._beautify(fig, "قرار الاحتفاظ مقابل الخروج")
        )

        return charts

    # ==================================================
    # CHAPTER 8 – SIGNALS
    # ==================================================
    def chapter_8(self, df):
        charts = {}

        if self._has(df, ["date", "price"]):
            fig = px.scatter(df, x="date", y="price", opacity=0.5)
            charts["hero"] = self._beautify(
                fig, "السلوك غير الطبيعي في السوق"
            )

        charts["supporting"] = []

        if self._has(df, ["date", "signal_strength"]):
            fig = px.line(df, x="date", y="signal_strength")
            charts["supporting"].append(
                self._beautify(fig, "شدة الإشارات المبكرة")
            )

        return charts

    # ==================================================
    # MASTER GENERATOR
    # ==================================================
    def generate_all(self, df):
        return {
            "chapter_1": self.chapter_1(df),
            "chapter_2": self.chapter_2(df),
            "chapter_3": self.chapter_3(df),
            "chapter_4": self.chapter_4(df),
            "chapter_5": self.chapter_5(df),
            "chapter_6": self.chapter_6(df),
            "chapter_7": self.chapter_7(df),
            "chapter_8": self.chapter_8(df),
        }
