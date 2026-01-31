# advanced_charts.py - النسخة المعدلة مع رسم بيانات حقيقي
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    PREMIUM EXECUTIVE CHARTS ENGINE
    مستوى عالمي – هادئ – انسيابي
    3 رسومات لكل فصل – بدون مخاطرة
    """

    # =====================
    # VISUAL IDENTITY
    # =====================
    COLORS = {
        "emerald": "#1B5E20",
        "mint": "#A5D6A7",
        "plum": "#6A1B9A",
        "lavender": "#E1BEE7",
        "gold": "#C9A227",
        "light_gray": "#F5F5F5",
        "text": "#333333",
    }

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return df is not None and all(col in df.columns for col in cols)

    def _numeric(self, s):
        return pd.to_numeric(s, errors="coerce")

    def _safe(self, fig, height=460):
        """
        ✅ نظيفة تماماً - تحديد الحجم من مكان الاستدعاء فقط
        """
        if fig is None:
            return None

        fig.update_layout(
            template="plotly_white",
            height=height,
            margin=dict(l=70, r=70, t=90, b=70),
            font=dict(size=15, color=self.COLORS["text"], family="Tajawal"),
            # ✅ التعديل 1: تكبير أرقام المحاور (x / y)
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(tickfont=dict(size=16)),
            title=dict(
                x=0.5,
                font=dict(size=18, color=self.COLORS["text"], family="Tajawal"),
            ),
            plot_bgcolor=self.COLORS["light_gray"],
            paper_bgcolor="white",
            hovermode="x unified",
            # ✅ التعديل 2: تحسين قراءة القيم عند المرور (Hover)
            hoverlabel=dict(font_size=15, font_family="Tajawal"),
        )

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False)

        return fig

    # =====================
    # DONUT HELPER (التنظيم المحسّن)
    # =====================
    def _donut_base_layout(self, fig, title):
        """
        ✅ Helper موحد لإعدادات الدونت الأساسية
        يضمن تطابقًا بصريًا 100% بين جميع الدونتس في التقرير
        """
        fig.update_layout(
            showlegend=False,  # ✅ لا مربعات ملونة - فقط الدونت نفسه يتكلم بصرياً
            title=dict(
                text=title,
                font=dict(size=24, family="Tajawal", color=self.COLORS["text"]),
                y=0.97,
                x=0.5,
                xanchor="center",
                pad=dict(t=10, b=10)  # ✅ تباعد مناسب
            ),
            # ✅ هوامش صغيرة جداً لتكبير الدونت
            margin=dict(l=20, r=20, t=80, b=20),  # ✅ هوامش صغيرة جداً
            plot_bgcolor="rgba(0,0,0,0)",  # ✅ خلفية شفافة
            paper_bgcolor="white",
            height=500,  # ✅ ارتفاع ثابت لجميع الدونتس
            font=dict(family="Tajawal"),
            annotations=[]  # ✅ تأكد من عدم وجود أي نصوص
        )

        # ✅ إزالة المحاور تماماً
        fig.update_xaxes(visible=False, showgrid=False, zeroline=False)
        fig.update_yaxes(visible=False, showgrid=False, zeroline=False)

        return fig

    def _donut_base_style(self, colors=None):
        """
        ✅ إعدادات القطاعات الأساسية للدونت
        """
        if colors is None:
            colors = [
                self.COLORS["mint"],
                self.COLORS["lavender"],
                self.COLORS["gold"],
            ]
        
        return {
            "hole": 0.85,  # ✅ ثقب كبير جداً - يخلق مساحة أنيقة
            "domain": dict(x=[0.05, 0.95], y=[0.10, 0.90]),  # ✅ يأخذ معظم الصفحة
            "marker": dict(
                colors=colors,
                line=dict(width=2, color='white')  # ✅ حواف بيضاء لفصل الألوان بوضوح
            ),
            "textinfo": "none",  # ✅ لا نصوص داخل القطاعات
            "hoverinfo": "none",  # ✅ لا معلومات عند التمرير
            "direction": 'clockwise',
            "rotation": 90,
            "sort": False  # ✅ الحفاظ على ترتيب الألوان
        }

    # =====================
    # REAL DATA – PRICE PER SQM BY DISTRICT (E2.1 رسم حقيقي جديد)
    # =====================
    def ch1_price_per_sqm_by_district(self, df):
        """
        رسم حقيقي: متوسط سعر المتر حسب المنطقة
        """
        # تحديد اسم العمود بمرونة
        district_col = (
            "المنطقة" if "المنطقة" in df.columns
            else "district" if "district" in df.columns
            else "الحي" if "الحي" in df.columns
            else None
        )

        if district_col is None or not self._has_columns(df, ["price", "area"]):
            return None

        tmp = df.copy()
        tmp["price"] = self._numeric(tmp["price"])
        tmp["area"] = self._numeric(tmp["area"])
        tmp["price_per_sqm"] = tmp["price"] / tmp["area"]

        tmp = tmp.dropna(subset=["price_per_sqm", district_col])

        if tmp[district_col].nunique() < 2:
            return None

        agg = (
            tmp
            .groupby(district_col)["price_per_sqm"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        fig = go.Figure(
            go.Bar(
                x=agg.values,
                y=agg.index,
                orientation="h",
                marker=dict(color=self.COLORS["emerald"]),
            )
        )

        fig.update_layout(
            title="متوسط سعر المتر حسب المنطقة",
            xaxis_title="سعر المتر",
            yaxis_title="المنطقة",
            yaxis=dict(autorange="reversed"),
        )

        return self._safe(fig, height=520)

    # =====================
    # RHYTHM 1 – DONUT INSIGHT (VERSION FINAL - نظيف تماماً)
    # =====================
    def rhythm_price_donut(self, df, title=None):
        if "price" not in df.columns:
            return None

        # ✅ تحديد العنوان الافتراضي إذا لم يتم تقديمه
        if title is None:
            title = "قراءة سريعة للسوق"

        # ✅ 1) قيم متساوية لثلاثة أجزاء
        values = [1, 1, 1]
        
        # ✅ استخدام الـhelper الموحد
        fig = go.Figure(
            data=[
                go.Pie(
                    values=values,
                    **self._donut_base_style()  # ✅ كل الإعدادات من helper
                )
            ]
        )

        # ✅ استخدام الـhelper الموحد للإعدادات
        fig = self._donut_base_layout(fig, title)

        return fig  # ❌ لا نستخدم _safe() على الدونتس أبداً

    # =====================
    # RHYTHM 2 – SOFT DISTRIBUTION (مكبر - ارتفاع 520)
    # =====================
    def rhythm_price_curve(self, df, title):
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 10:
            return None

        hist_y, hist_x = np.histogram(p, bins=30, density=True)
        hist_x = (hist_x[:-1] + hist_x[1:]) / 2

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hist_x,
                y=hist_y,
                mode="lines",
                line=dict(color=self.COLORS["plum"], width=4),
                fill="tozeroy",
                fillcolor="rgba(106,27,154,0.18)",
            )
        )

        fig.add_vline(
            x=p.mean(),
            line=dict(color=self.COLORS["gold"], width=2, dash="dot"),
            annotation_text="متوسط السوق",
            annotation_position="top",
        )

        fig.update_layout(title=title)
        # ✅ تحديد الحجم صراحة - 520 للرسومات الكبيرة
        return self._safe(fig, height=520)

    # =====================
    # RHYTHM PLACEHOLDER – CURVE (بدون بيانات - ارتفاع 520)
    # =====================
    def rhythm_placeholder_curve(self, title):
        """
        ✅ منحنى شكلي فقط
        بدون بيانات، بدون حسابات، جاهز للربط لاحقًا
        """
        fig = go.Figure()

        # خط وهمي خفيف (للهيكل فقط)
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                line=dict(
                    color=self.COLORS["plum"],
                    width=3
                ),
                hoverinfo="none"
            )
        )

        fig.update_layout(
            title=title,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
        )

        # ✅ تحديد الحجم صراحة - 520 للرسومات الكبيرة
        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 1 – MARKET RELATION
    # =====================
    def ch1_price_vs_area_flow(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        fig = go.Figure()

        fig.update_layout(
            title=dict(
                text="تحليل العلاقة بين المساحة والسعر",
                font=dict(
                    size=22,
                    family="Tajawal",
                    color=self.COLORS["emerald"]
                ),
                x=0.5
            ),
            xaxis_title="المساحة بالمتر المربع",
            yaxis_title="السعر",
            showlegend=False
        )

        fig.update_xaxes(
            showgrid=False,
            zeroline=False
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.06)",
            zeroline=False
        )

        # ✅ حجم عادي (460) - ليس من الرسومات الكبيرة
        return self._safe(fig, height=460)

    # =====================
    # CHAPTER 2 – TIME FLOW (مكبر - ارتفاع 520)
    # =====================
    def ch2_price_stream(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        df = df.sort_values("date")
        df["price"] = self._numeric(df["price"])

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["price"],
                mode="lines",
                line=dict(color=self.COLORS["emerald"], width=3),
                fill="tozeroy",
                fillcolor="rgba(27,94,32,0.18)",
            )
        )

        # ✅ التعديل 1: اختصار عنوان محور Y
        # ✅ التعديل 2: تقليل المسافة العمودية للعنوان
        fig.update_layout(
            title="تدفق الأسعار عبر الزمن",
            xaxis_title="الزمن",
            yaxis_title="القيمة السوقية",
            yaxis=dict(title_standoff=10),
        )

        # ✅ تحديد الحجم صراحة - 520 للرسومات الكبيرة
        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 3 – SAMPLE TABLE
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample = df[["area", "price"]].head(12)

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color="#F4F6F8",
                        align="center",
                        font=dict(
                            size=14,
                            color="#1F2933",
                            family="Tajawal"
                        ),
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        fill_color="white",
                        align="center",
                        font=dict(
                            size=13,
                            color="#1F2933",
                            family="Tajawal"
                        ),
                    ),
                )
            ]
        )

        fig.update_layout(title="عينة ذكية من بيانات السوق", height=560)
        return fig

    # =====================
    # CHAPTER 4 – MARKET INDICATORS BAR
    # =====================
    def ch4_market_indicators_bar(self, df):
        categories = ["السعر", "السيولة", "الاستقرار"]
        values = [1, 1, 1]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=categories,
                x=values,
                orientation="h",
                marker=dict(
                    color=self.COLORS["emerald"],
                    opacity=0.85
                ),
                hoverinfo="none"
            )
        )

        fig.update_layout(
            title="مقارنة مؤشرات السوق الرئيسية",
            xaxis=dict(
                visible=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                tickfont=dict(size=15),
                autorange="reversed"
            ),
            showlegend=False,
            bargap=0.4
        )

        # ✅ حجم عادي (460) - ليس من الرسومات الكبيرة
        return self._safe(fig, height=460)

    # =====================
    # CHAPTER 5 – FUTURE OPPORTUNITY PLACEHOLDER
    # =====================
    def ch5_future_opportunity_placeholder(self):
        fig = go.Figure()

        fig.update_layout(
            title="مساحة الفرص الاستثمارية",
            xaxis_title="",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            font=dict(family="Tajawal", size=16, color=self.COLORS["text"]),
        )

        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.04)",
            zeroline=False,
            ticks="",
            showline=True,
            linewidth=1,
            linecolor="rgba(0,0,0,0.1)"
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.04)",
            zeroline=False,
            ticks="",
            showline=True,
            linewidth=1,
            linecolor="rgba(0,0,0,0.1)"
        )

        # ✅ حجم عادي (460) - ليس من الرسومات الكبيرة
        return self._safe(fig, height=460)

    # =====================
    # CHAPTER 6 – GAUGE
    # =====================
    def ch6_gauge(self, df):
        fig = go.Figure(go.Indicator(
            mode="gauge",
            gauge={
                'axis': {'range': [0, 100], 'visible': False},
                'bar': {'color': self.COLORS["gold"]},
                'steps': [
                    {'range': [0, 40], 'color': self.COLORS["lavender"]},
                    {'range': [40, 70], 'color': self.COLORS["mint"]},
                    {'range': [70, 100], 'color': self.COLORS["emerald"]},
                ],
            }
        ))

        fig.update_layout(
            title="مؤشر القرار التنفيذي",
            height=520,
            margin=dict(l=30, r=30, t=90, b=30),
            font=dict(family="Tajawal", size=18)
        )

        return fig

    # =====================
    # CHAPTER 7 – EXECUTIVE DONUT
    # =====================
    def ch7_executive_donut(self, df):
        values = [1, 1, 1]

        fig = go.Figure(
            data=[
                go.Pie(
                    values=values,
                    **self._donut_base_style([
                        self.COLORS["gold"],
                        self.COLORS["plum"],
                        self.COLORS["mint"]
                    ])
                )
            ]
        )

        fig = self._donut_base_layout(
            fig,
            "الملخص التنفيذي"
        )

        return fig

    # =====================
    # CHAPTER 8 – FINAL CURVE (مكبر - ارتفاع 520)
    # =====================
    def ch8_final_curve(self, df):
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 10:
            return None

        hist_y, hist_x = np.histogram(p, bins=20, density=True)
        hist_x = (hist_x[:-1] + hist_x[1:]) / 2

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hist_x,
                y=hist_y,
                mode="lines",
                line=dict(color=self.COLORS["lavender"], width=2),
                name="التوزيع الختامي",
                hoverinfo="skip"
            )
        )

        fig.update_layout(
            title="المنحنى الختامي - نظرة نهائية",
            xaxis_title="نطاق السعر",
            yaxis_title="الكثافة النسبية",
        )
        
        # ✅ تحديد الحجم صراحة - 520 للرسومات الكبيرة
        return self._safe(fig, height=520)

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        if df is None or df.empty:
            return {}

        def clean(lst):
            return [x for x in lst if x is not None]

        return {
            "chapter_1": clean([
                self.ch1_price_per_sqm_by_district(df),   # 🔥 رسم حقيقي جديد
                self.ch1_price_vs_area_flow(df),
                self.rhythm_price_curve(df, "توزيع الأسعار بانسيابية"),
            ]),
            "chapter_2": clean([
                self.ch2_price_stream(df),                    # مكبر
                self.rhythm_price_donut(df, "مستويات الأسعار"),    # دونت
                self.rhythm_price_curve(df, "توزيع الأسعار عبر الزمن"),  # مكبر
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),                    # حجم خاص
                self.rhythm_price_donut(df, "نطاق العينة"),        # دونت
                self.rhythm_price_curve(df, "تشتت الأسعار"),       # مكبر
            ]),
            "chapter_4": clean([
                self.rhythm_price_donut(df, "نطاقات السوق"),       # دونت
                self.ch4_market_indicators_bar(df),            # حجم عادي
            ]),
            "chapter_5": clean([
                self.rhythm_price_donut(df, "قراءة هيكلية للسوق"), # دونت
                self.ch5_future_opportunity_placeholder(),     # حجم عادي
            ]),
            "chapter_6": clean([
                self.rhythm_price_donut(df, "رأس المال"),          # دونت
                self.rhythm_placeholder_curve("توزيع الاستثمار"),  # مكبر
                self.ch6_gauge(df),                           # Gauge
            ]),
            "chapter_7": clean([
                self.ch7_executive_donut(df),                 # دونت
            ]),
            "chapter_8": clean([
                self.ch8_final_curve(df),                     # مكبر
            ]),
            "chapter_9": [],
            "chapter_10": [],
        }
