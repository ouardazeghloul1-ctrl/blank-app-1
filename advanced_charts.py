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
    # RHYTHM 1 – DONUT INSIGHT (VERSION FINAL - نظيف تماماً)
    # =====================
    def rhythm_price_donut(self, df, title):
        if "price" not in df.columns:
            return None

        # ✅ 1) قيم متساوية لثلاثة أجزاء
        values = [1, 1, 1]
        
        fig = go.Figure(
            data=[
                go.Pie(
                    values=values,
                    hole=0.85,  # ✅ ثقب كبير جداً - يخلق مساحة أنيقة
                    domain=dict(x=[0.05, 0.95], y=[0.10, 0.90]),  # ✅ يأخذ معظم الصفحة
                    marker=dict(
                        colors=[
                            self.COLORS["mint"],
                            self.COLORS["lavender"],
                            self.COLORS["gold"],
                        ],
                        line=dict(width=2, color='white')  # ✅ حواف بيضاء لفصل الألوان بوضوح
                    ),
                    textinfo="none",  # ✅ لا نصوص داخل القطاعات
                    hoverinfo="none",  # ✅ لا معلومات عند التمرير
                    direction='clockwise',
                    rotation=90,
                    sort=False  # ✅ الحفاظ على ترتيب الألوان
                )
            ]
        )

        # ✅ 2) إعدادات التخطيط - مصممة خصيصاً للدونت الكبير والنظيف
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
            # ✅ 3) هوامش صغيرة جداً لتكبير الدونت
            margin=dict(l=20, r=20, t=80, b=20),  # ✅ هوامش صغيرة جداً
            plot_bgcolor="rgba(0,0,0,0)",  # ✅ خلفية شفافة
            paper_bgcolor="white",
            height=500,  # ✅ ارتفاع مناسب
            font=dict(family="Tajawal"),
            annotations=[]  # ✅ تأكد من عدم وجود أي نصوص
        )

        # ✅ 4) إزالة المحاور تماماً
        fig.update_xaxes(visible=False, showgrid=False, zeroline=False)
        fig.update_yaxes(visible=False, showgrid=False, zeroline=False)

        return fig

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

        indicators = [
            "السعر",
            "المساحة",
            "السيولة",
            "الطلب",
            "الاستقرار"
        ]

        # ✅ قيم محايدة (شكل فقط – ليست بيانات)
        values = [1, 1, 1, 1, 1]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=indicators,
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
                tickfont=dict(size=15)
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

    def ch6_gauge(self, df):
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if p.empty:
            return None

        price_std = p.std()
        price_mean = p.mean()
        
        if price_std > 0:
            market_index = max(0, min(100, 100 - (price_std / price_mean * 100)))
        else:
            market_index = 85

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=market_index,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "مؤشر استقرار السوق", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': self.COLORS["gold"]},
                'steps': [
                    {'range': [0, 40], 'color': self.COLORS["lavender"]},
                    {'range': [40, 70], 'color': self.COLORS["mint"]},
                    {'range': [70, 100], 'color': self.COLORS["emerald"]}
                ],
                'threshold': {
                    'line': {'color': self.COLORS["plum"], 'width': 4},
                    'thickness': 0.75,
                    'value': market_index
                }
            }
        ))

        fig.update_layout(
            title=f"مؤشر القرار التنفيذي: {market_index:.0f}/100",
            height=380
        )
        return fig

    def ch7_executive_donut(self, df):
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if p.empty:
            return None

        segments = {
            "الشرائح العليا": p[p > p.quantile(0.75)].count(),
            "الشرائح المتوسطة": p[(p >= p.quantile(0.25)) & (p <= p.quantile(0.75))].count(),
            "الشرائح الاقتصادية": p[p < p.quantile(0.25)].count()
        }

        fig = go.Figure(
            data=[
                go.Pie(
                    values=list(segments.values()),
                    labels=list(segments.keys()),
                    hole=0.7,
                    marker=dict(
                        colors=[
                            self.COLORS["gold"],
                            self.COLORS["plum"],
                            self.COLORS["mint"]
                        ]
                    ),
                    textinfo='label',
                    textposition='outside'
                )
            ]
        )

        total_properties = len(p)
        avg_price = p.mean()
        
        fig.add_annotation(
            text=f"<b>ملخص تنفيذي</b><br><br>"
                 f"إجمالي العقارات:<br><b>{total_properties:,}</b><br><br>"
                 f"متوسط السوق:<br><b>{avg_price:,.0f}</b>",
            x=0.5,
            y=0.5,
            font=dict(size=16, color=self.COLORS["text"]),
            showarrow=False,
            align="center"
        )

        fig.update_layout(
            title="الملخص التنفيذي - نظرة شاملة",
            showlegend=False
        )
        return self._safe(fig, height=480)

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
                self.rhythm_price_donut(df, "قراءة سريعة للسوق"),
                self.rhythm_price_curve(df, "توزيع الأسعار بانسيابية"),
            ]),
            "chapter_2": clean([
                self.ch2_price_stream(df),  # ✅ مع تعديل الأقواس
                self.rhythm_price_donut(df, "مستويات الأسعار"),
                # ✅ استبدال ch2_area_ribbon بـ rhythm_price_curve
                self.rhythm_price_curve(df, "توزيع الأسعار عبر الزمن"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),  # ✅ محسّن للاحترافية
                self.rhythm_price_donut(df, "نطاق العينة"),
                self.rhythm_price_curve(df, "تشتت الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_donut(df, "نطاقات السوق"),
                # ✅ استبدال ch4_radar بـ ch4_market_indicators_bar
                self.ch4_market_indicators_bar(df),
            ]),
            "chapter_5": clean([
                self.rhythm_price_donut(df, "مقارنة زمنية"),
                self.rhythm_price_curve(df, "ديناميكية الأسعار"),
                self.ch5_bubble(df),
            ]),
            "chapter_6": clean([
                self.rhythm_price_donut(df, "رأس المال"),
                self.rhythm_price_curve(df, "توزيع الاستثمار"),
                self.ch6_gauge(df),
            ]),
            "chapter_7": clean([
                self.ch7_executive_donut(df),
            ]),
            "chapter_8": clean([
                self.ch8_final_curve(df),
            ]),
            "chapter_9": [],
            "chapter_10": [],
        }
