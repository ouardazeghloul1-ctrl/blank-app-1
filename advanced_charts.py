# advanced_charts.py - النسخة النهائية المعدلة
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
        if fig is None:
            return None

        fig.update_layout(
            template="plotly_white",
            height=height,
            margin=dict(l=70, r=70, t=90, b=70),
            font=dict(size=15, color=self.COLORS["text"], family="Tajawal"),
            title=dict(
                x=0.5,
                font=dict(size=18, color=self.COLORS["text"], family="Tajawal"),
            ),
            plot_bgcolor=self.COLORS["light_gray"],
            paper_bgcolor="white",
            hovermode="x unified",
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
    # RHYTHM 2 – SOFT DISTRIBUTION
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
        return self._safe(fig, height=360)

    # =====================
    # RHYTHM PLACEHOLDER – CURVE (بدون بيانات)
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
            paper_bgcolor="white",  # ✅ التصحيح: paper_bgcolor بدل paperbgcolor
        )

        return self._safe(fig, height=360)

    # =====================
    # CHAPTER 1 – MARKET RELATION (المطابقة للصورة مع تعديل الأقواس)
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
                    color=self.COLORS["emerald"]  # ✅ نفس اللون الأخضر
                ),
                x=0.5
            ),
            # ✅ 1️⃣ تعديل: جملة لغوية بدون أقواس
            xaxis_title="المساحة بالمتر المربع",
            yaxis_title="السعر بالريال",
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

        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 2 – TIME FLOW (مع تعديل عناوين المحاور)
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

        fig.update_layout(
            title="تدفق الأسعار عبر الزمن",
            # ✅ 2️⃣ تعديل: جملة لغوية بدون أقواس
            xaxis_title="الزمن",
            yaxis_title="القيمة السوقية بالريال السعودي",
        )

        return self._safe(fig, height=480)

    # =====================
    # CHAPTER 3 – SAMPLE TABLE (محسّن للاحترافية)
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        # ✅ 1️⃣ زيادة عدد الصفوف إلى 12
        sample = df[["area", "price"]].head(12)

        fig = go.Figure(
            data=[
                go.Table(
                    # ✅ 2️⃣ تحسين ألوان الجدول (McKinsey/BCG style)
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color="#F4F6F8",   # رمادي فاتح جدًا (تنفيذي)
                        align="center",
                        font=dict(
                            size=14,
                            color="#1F2933",     # داكن مريح للعين
                            family="Tajawal"
                        ),
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        fill_color="white",     # خلفية نظيفة
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

        fig.update_layout(title="عينة ذكية من بيانات السوق", height=560)  # ✅ 3️⃣ زيادة الارتفاع
        return fig

    # =====================
    # الرسومات الجديدة (6 رسومات)
    # =====================
    
    def ch2_area_ribbon(self, df):
        if not self._has_columns(df, ["date", "price"]):
            return None

        df = df.sort_values("date")
        df["price"] = self._numeric(df["price"])
        df = df.dropna()
        
        if df.empty:
            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["price"],
                mode="lines",
                line=dict(color=self.COLORS["mint"], width=1.5),
                fill="tozeroy",
                fillcolor="rgba(165,214,167,0.15)",
                name="منحنى التدفق",
            )
        )

        fig.update_layout(
            title="شريط التدفق الزمني - تحليل انسيابي",
            # ✅ تعديل: جملة لغوية بدون أقواس
            xaxis_title="التاريخ",
            yaxis_title="السعر بالريال",
        )

        return self._safe(fig, height=380)

    # =====================
    # CHAPTER 4 – MARKET INDICATORS (BAR COMPARISON)
    # =====================
    def ch4_market_indicators_bar(self, df):
        """
        مخطط أعمدة تنفيذي لمقارنة مؤشرات السوق
        بدون بيانات مزيفة – جاهز للبيانات الحقيقية لاحقًا
        """

        categories = ["السعر", "السيولة", "الاستقرار"]
        
        # ✅ قيم محايدة (شكل فقط – ليست بيانات)
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
                autorange="reversed"  # ✅ يعكس الترتيب بصريًا
            ),
            showlegend=False,
            bargap=0.4
        )

        return self._safe(fig, height=420)

    def ch5_bubble(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        df = df.copy()
        df["price_num"] = self._numeric(df["price"])
        df["area_num"] = self._numeric(df["area"])
        df = df.dropna()
        
        if df.empty:
            return None

        max_size = 40
        df["size"] = (df["price_num"] / df["price_num"].max()) * max_size

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["area_num"],
                y=df["price_num"],
                mode='markers',
                marker=dict(
                    size=df["size"],
                    color=self.COLORS["plum"],
                    opacity=0.6,
                    line=dict(width=1, color='white')
                ),
                text=[f"السعر: {p:,.0f}<br>المساحة: {a:,.0f}" 
                      for p, a in zip(df["price_num"], df["area_num"])],
                hoverinfo='text'
            )
        )

        fig.update_layout(
            title="مخطط الفقاعات - تحليل الفرص",
            # ✅ تعديل: جملة لغوية بدون أقواس
            xaxis_title="المساحة بالمتر المربع",
            yaxis_title="السعر بالريال",
        )

        return self._safe(fig, height=480)

    # =====================
    # CHAPTER 5 – FUTURE OPPORTUNITY PLACEHOLDER
    # =====================
    def ch5_future_opportunity_placeholder(self):
        """
        ✅ Placeholder ذكي لمساحة الفرص الاستثمارية
        عنوان فقط، بلا تفسير، بلا بيانات مزيفة
        """
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

        # خطوط خفيفة جدًا فقط لإيحاء الإطار
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

        return self._safe(fig, height=420)

    # =====================
    # CHAPTER 6 – GAUGE (بدون بيانات مزيفة - شكل نظيف)
    # =====================
    def ch6_gauge(self, df):
        """
        ✅ مؤشر شكل نظيف بدون بيانات مزيفة
        لا أرقام، لا قيم، مجرد شكل تنفيذي جاهز
        """
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
    # CHAPTER 7 – EXECUTIVE DONUT (بدون بيانات)
    # =====================
    def ch7_executive_donut(self, df):
        """
        ✅ دونت تنفيذي – بدون بيانات
        Placeholder جاهز للربط لاحقًا
        """
        # قيم شكلية فقط (لا معنى تحليلي)
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

        return fig  # ❌ لا نستخدم _safe() على الدونتس أبداً

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
            # ✅ تعديل: جملة لغوية بدون أقواس
            xaxis_title="نطاق السعر",
            yaxis_title="الكثافة النسبية",
        )
        
        return self._safe(fig, height=360)

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
                self.ch1_price_vs_area_flow(df),  # ✅ مع تعديل الأقواس
                self.rhythm_price_donut(df, "قراءة سريعة للسوق"),  # ✅ حجم موحد
                self.rhythm_price_curve(df, "توزيع الأسعار بانسيابية"),
            ]),
            "chapter_2": clean([
                self.ch2_price_stream(df),  # ✅ مع تعديل الأقواس
                self.rhythm_price_donut(df, "مستويات الأسعار"),  # ✅ حجم موحد
                # ✅ استبدال ch2_area_ribbon بـ rhythm_price_curve
                self.rhythm_price_curve(df, "توزيع الأسعار عبر الزمن"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),  # ✅ محسّن للاحترافية
                self.rhythm_price_donut(df, "نطاق العينة"),  # ✅ حجم موحد
                self.rhythm_price_curve(df, "تشتت الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_donut(df, "نطاقات السوق"),  # ✅ حجم موحد
                # ✅ استبدال ch4_radar بـ ch4_market_indicators_bar
                self.ch4_market_indicators_bar(df),
            ]),
            "chapter_5": clean([
                self.rhythm_price_donut(df, "قراءة هيكلية للسوق"),  # ✅ عنوان أدق
                self.ch5_future_opportunity_placeholder(),  # ✅ لا بيانات مزيفة
            ]),
            "chapter_6": clean([
                self.rhythm_price_donut(df, "رأس المال"),  # ✅ حجم موحد
                self.rhythm_placeholder_curve("توزيع الاستثمار"),  # ✅ منحنى شكلي بدون بيانات
                self.ch6_gauge(df),  # ✅ مؤشر نظيف بدون بيانات مزيفة
            ]),
            "chapter_7": clean([
                self.ch7_executive_donut(df),  # ✅ دونت تنفيذي بدون بيانات
            ]),
            "chapter_8": clean([
                self.ch8_final_curve(df),
            ]),
            "chapter_9": [],
            "chapter_10": [],
        }
