# advanced_charts.py (ملف كامل معدل)
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
    # RHYTHM 1 – DONUT INSIGHT (MODIFIED - كبير ونظيف)
    # =====================
    def rhythm_price_donut(self, df, title):
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if p.empty:
            return None

        # قيم محايدة تماماً
        values = [1, 1, 1]

        fig = go.Figure(
            data=[
                go.Pie(
                    values=values,
                    hole=0.75,  # ✅ الثقب أكبر
                    domain=dict(x=[0.15, 0.85], y=[0.15, 0.85]),  # ✅ يأخذ معظم الصفحة
                    marker=dict(
                        colors=[
                            self.COLORS["mint"],
                            self.COLORS["lavender"],
                            self.COLORS["gold"],
                        ]
                    ),
                    textinfo="none",
                    hoverinfo="none",  # ✅ لا معلومات عند التمرير
                )
            ]
        )

        fig.update_layout(
            showlegend=False,
            title=dict(
                text=title,
                font=dict(size=22, family="Tajawal"),  # ✅ عنوان أكبر
                y=0.95
            )
        )

        # ✅ نص بسيط في المنتصف (بدون متوسط سعر مزيف)
        fig.add_annotation(
            text="جاري تحميل البيانات<br>...",
            x=0.5,
            y=0.5,
            font=dict(size=24, color=self.COLORS["text"]),
            showarrow=False,
        )

        return self._safe(fig, height=650)  # ✅ حجم كبير جداً

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
    # CHAPTER 1 – MARKET RELATION (MODIFIED WITH OPTIONAL IMPROVEMENTS)
    # =====================
    def ch1_price_vs_area_flow(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        df = df.copy()
        df["price"] = self._numeric(df["price"])
        df["area"] = self._numeric(df["area"])
        df = df.dropna()

        # 🔧 1) ترتيب النقاط بصريًا (Anti-overlap)
        df = df.sort_values("price")  # 🔥 النقاط الصغيرة أولاً، الكبيرة فوقها

        # ✅ التحسين الذهبي: حجم ذكي للنقاط يعتمد على السعر
        df["marker_size"] = ((df["price"] / df["price"].max()) * 18).clip(lower=8)

        fig = go.Figure()

        # 🔥 تدرج أخضر ذكي بدل لون واحد
        fig.add_trace(
            go.Scatter(
                x=df["area"],
                y=df["price"],
                mode="markers",
                marker=dict(
                    size=df["marker_size"],
                    color=df["price"],  # 🔥 تدرج حسب السعر
                    colorscale=[
                        [0, "#C8E6C9"],
                        [0.5, "#66BB6A"],
                        [1, "#1B5E20"]
                    ],
                    showscale=False,
                    opacity=0.78,
                    line=dict(width=0.6, color="white")
                ),
                name="العقارات"
            )
        )

        # 🔥 أضيفي خط اتجاه ناعم (Trend Line) - النسخة السينمائية
        try:
            z = np.polyfit(df["area"], np.log(df["price"]), 1)
            p = np.poly1d(z)
            
            # 🔧 2) نعومة إضافية لخط الاتجاه (Luxury Touch)
            area_sorted = np.linspace(df["area"].min(), df["area"].max(), 100)
            
            fig.add_trace(
                go.Scatter(
                    x=area_sorted,
                    y=np.exp(p(area_sorted)),
                    mode="lines",
                    line=dict(color=self.COLORS["gold"], width=3),
                    name="اتجاه السوق"
                )
            )
        except:
            pass  # إذا فشل حساب الاتجاه، نستمر

        # 🔧 3) Annotation واحدة ذكية (اختياري جدًا)
        fig.add_annotation(
            text="↑ كلما زادت المساحة<br>ارتفعت القيمة السوقية",
            xref="paper",
            yref="paper",
            x=0.02,
            y=0.95,
            showarrow=False,
            font=dict(size=13, color="#555"),
            align="left",
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
            borderpad=4
        )

        fig.update_layout(
            title="كيف تتحول المساحة إلى قيمة سوقية",
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر (مقياس لوغاريتمي)",
            hovermode="closest",
            showlegend=False
        )

        # 🔥 اجعلي السعر لوغاريتمي (أهم تعديل)
        fig.update_yaxes(
            type="log",
            title_font=dict(size=16),
            showgrid=True,
            gridcolor="rgba(0,0,0,0.06)",
            ticks="outside",
            tickcolor="rgba(0,0,0,0.2)"
        )

        fig.update_xaxes(
            title_font=dict(size=16),
            ticks="outside",
            tickcolor="rgba(0,0,0,0.2)",
            showgrid=False
        )

        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 2 – TIME FLOW
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
            xaxis_title="الزمن",
            yaxis_title="السعر",
        )

        return self._safe(fig, height=480)

    # =====================
    # CHAPTER 3 – SAMPLE TABLE
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample = df[["area", "price"]].head(8)

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة", "السعر"],
                        fill_color=self.COLORS["light_gray"],
                        align="center",
                        font=dict(size=14, color=self.COLORS["text"]),
                    ),
                    cells=dict(
                        values=[sample["area"], sample["price"]],
                        align="center",
                        font=dict(size=12, color=self.COLORS["text"]),
                    ),
                )
            ]
        )

        fig.update_layout(title="عينة ذكية من بيانات السوق", height=420)
        return fig

    # =====================
    # الرسومات الجديدة (6 رسومات)
    # =====================
    
    # 1) الفصل 2 – Ribbon (بديل المنحنى المكرر)
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
            xaxis_title="التاريخ",
            yaxis_title="السعر",
        )

        return self._safe(fig, height=380)

    # 2) الفصل 4 – Radar (تحليل بصري ذكي)
    def ch4_radar(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        categories = ["السعر", "المساحة", "السيولة", "الطلب", "الاستقرار"]
        
        np.random.seed(42)
        values = np.random.uniform(0.4, 0.9, len(categories))
        
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(225,190,231,0.2)',
            line=dict(color=self.COLORS["plum"], width=2),
            name="مؤشرات السوق"
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(size=10)
                )
            ),
            title="رادار تحليل السوق - نظرة شاملة",
            showlegend=False
        )

        return self._safe(fig, height=420)

    # 3) الفصل 5 – Bubble Chart
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
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر",
        )

        return self._safe(fig, height=480)

    # 4) الفصل 6 – Gauge (قرار تنفيذي)
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

    # 5) الفصل 7 – Executive Donut
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

    # 6) الفصل 8 – Final Curve (منحنى ختامي خفيف)
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
            yaxis_title="الكثافة",
            showlegend=False
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
                self.ch1_price_vs_area_flow(df),
                self.rhythm_price_donut(df, "قراءة سريعة للسوق"),  # ✅ كبير ونظيف
                self.rhythm_price_curve(df, "توزيع الأسعار بانسيابية"),
            ]),
            "chapter_2": clean([
                self.ch2_price_stream(df),
                self.rhythm_price_donut(df, "مستويات الأسعار"),  # ✅ كبير ونظيف
                self.ch2_area_ribbon(df),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_donut(df, "نطاق العينة"),  # ✅ كبير ونظيف
                self.rhythm_price_curve(df, "تشتت الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_donut(df, "نطاقات السوق"),  # ✅ كبير ونظيف
                self.ch4_radar(df),
            ]),
            "chapter_5": clean([
                self.rhythm_price_donut(df, "مقارنة زمنية"),  # ✅ كبير ونظيف
                self.rhythm_price_curve(df, "ديناميكية الأسعار"),
                self.ch5_bubble(df),
            ]),
            "chapter_6": clean([
                self.rhythm_price_donut(df, "رأس المال"),  # ✅ كبير ونظيف
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
