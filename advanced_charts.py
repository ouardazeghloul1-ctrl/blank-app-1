# advanced_charts.py - الإصدار النهائي المعدّل (جاهز للبيع)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    PREMIUM EXECUTIVE CHARTS ENGINE
    مستوى عالمي – هادئ – انسيابي
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

    def _ensure_numeric_core(self, df):
        """
        توحيد وتنظيف البيانات الأساسية للرسومات
        """
        if df is None or df.empty:
            return pd.DataFrame()
            
        df = df.copy()

        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

        if "area" in df.columns:
            df["area"] = pd.to_numeric(df["area"], errors="coerce")

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        if self._has_columns(df, ["price", "area"]):
            df = df.dropna(subset=["price", "area"])
        
        return df

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
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(tickfont=dict(size=16)),
            title=dict(
                x=0.5,
                font=dict(size=18, color=self.COLORS["text"], family="Tajawal"),
            ),
            plot_bgcolor=self.COLORS["light_gray"],
            paper_bgcolor="white",
            hovermode="x unified",
            hoverlabel=dict(font_size=15, font_family="Tajawal"),
        )

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False)

        return fig

    # =====================
    # CHAPTER 1 – PRICE PER SQM BY DISTRICT
    # =====================
    def ch1_price_per_sqm_by_district(self, df):
        """
        رسم 1: متوسط سعر المتر حسب المنطقة
        """
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
    # CHAPTER 2 – TIME FLOW
    # =====================
    def ch2_price_stream(self, df):
        """
        رسم 2: تدفق الأسعار عبر الزمن
        """
        if not self._has_columns(df, ["date", "price"]):
            return None

        tmp = df.copy()
        tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
        tmp["price"] = self._numeric(tmp["price"])
        tmp = tmp.dropna(subset=["date", "price"])
        tmp = tmp.sort_values("date")

        if len(tmp) < 5:
            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=tmp["date"],
                y=tmp["price"],
                mode="lines+markers",
                line=dict(color=self.COLORS["emerald"], width=3),
                marker=dict(size=6, color=self.COLORS["gold"]),
                fill="tozeroy",
                fillcolor="rgba(27,94,32,0.18)",
            )
        )

        fig.update_layout(
            title="تدفق الأسعار عبر الزمن",
            xaxis_title="الزمن",
            yaxis_title="القيمة السوقية",
            yaxis=dict(title_standoff=10),
        )

        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 3 – PRICE DISTRIBUTION
    # =====================
    def rhythm_price_curve(self, df, title):
        """
        رسم 3: توزيع الأسعار
        """
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
            # ✅ التعديل 1: عنوان تنفيذي بلا رقم
            annotation_text="متوسط السعر",
            annotation_position="top",
            annotation_font=dict(size=12, family="Tajawal")
        )

        fig.update_layout(title=title)
        fig.update_xaxes(tickformat="~s")
        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 4 – MARKET RELATION
    # =====================
    def ch1_price_vs_area_flow(self, df):
        """
        رسم 4: تحليل العلاقة بين المساحة والسعر
        """
        if not self._has_columns(df, ["price", "area"]):
            return None

        tmp = df.copy()
        tmp["price"] = self._numeric(tmp["price"])
        tmp["area"] = self._numeric(tmp["area"])
        tmp = tmp.dropna(subset=["price", "area"])

        if len(tmp) < 5:
            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=tmp["area"],
                y=tmp["price"],
                mode='markers',
                marker=dict(
                    size=8,
                    color=self.COLORS["emerald"],
                    opacity=0.7
                ),
                name="العقارات",
                text=[f"{a} متر — {p:,.0f}" for a, p in zip(tmp["area"], tmp["price"])],
                hoverinfo="text"
            )
        )

        if len(tmp) > 1:
            z = np.polyfit(tmp["area"], tmp["price"], 1)
            p = np.poly1d(z)
            fig.add_trace(
                go.Scatter(
                    x=tmp["area"],
                    y=p(tmp["area"]),
                    mode='lines',
                    line=dict(color=self.COLORS["gold"], width=2, dash='dash'),
                    name="اتجاه السوق"
                )
            )

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
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False)

        return self._safe(fig, height=460)

    # =====================
    # CHAPTER 5 – MARKET INDICATORS
    # =====================
    def ch4_market_indicators_bar(self, df):
        """
        رسم 5: مقارنة مؤشرات السوق الرئيسية
        """
        if not self._has_columns(df, ["price", "area"]):
            return None

        tmp = df.copy()
        tmp["price"] = self._numeric(tmp["price"])
        tmp["area"] = self._numeric(tmp["area"])
        tmp = tmp.dropna(subset=["price", "area"])

        if len(tmp) < 3:
            return None

        avg_price = tmp["price"].mean()
        avg_area = tmp["area"].mean()
        price_per_sqm = avg_price / avg_area if avg_area > 0 else 0
        
        categories = ["متوسط السعر", "متوسط المساحة", "سعر المتر"]
        
        # ✅ التعديل 2: قيم حقيقية بلا نسب افتراضية
        values = [
            avg_price,
            avg_area,
            price_per_sqm
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=categories,
                x=values,
                orientation="h",
                marker=dict(
                    color=[
                        self.COLORS["emerald"],
                        self.COLORS["mint"],
                        self.COLORS["gold"]
                    ],
                    opacity=0.85
                ),
                # ✅ قيم فعلية لا نسب مئوية
                text=[f"{v:,.0f}" for v in values],
                textposition="outside"
            )
        )

        max_value = max(values) if values else 1000000
        x_range = [0, max_value * 1.1]

        fig.update_layout(
            title="لوحة قراءة السوق",
            xaxis=dict(
                visible=False,
                showgrid=False,
                zeroline=False,
                range=x_range
            ),
            yaxis=dict(
                tickfont=dict(size=15),
                autorange="reversed"
            ),
            showlegend=False,
            bargap=0.4
        )

        return self._safe(fig, height=460)

    # =====================
    # CHAPTER 6 – GAUGE
    # =====================
    def ch6_gauge(self, df):
        """
        رسم 6: مؤشر القرار التنفيذي
        """
        if not self._has_columns(df, ["price", "area"]):
            return None

        tmp = df.copy()
        tmp["price"] = self._numeric(tmp["price"])
        tmp["area"] = self._numeric(tmp["area"])
        tmp = tmp.dropna(subset=["price", "area"])

        if len(tmp) < 5:
            return None

        avg_price = tmp["price"].mean()
        avg_area = tmp["area"].mean()
        
        if avg_area > 0:
            price_per_sqm = avg_price / avg_area
            score = min(100, max(0, (price_per_sqm / 20000) * 100))
        else:
            score = 50

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'visible': False},
                'bar': {'color': self.COLORS["gold"], 'thickness': 0.25},
                'steps': [
                    {'range': [0, 40], 'color': self.COLORS["lavender"]},
                    {'range': [40, 70], 'color': self.COLORS["mint"]},
                    {'range': [70, 100], 'color': self.COLORS["emerald"]},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
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
        """
        رسم 7: الملخص التنفيذي (قوة القرار)
        """
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 3:
            return None

        # حساب يعكس قوة القرار
        avg_price = p.mean()
        median_price = p.median()
        volatility = p.std()
        price_range = p.max() - p.min()

        # ✅ التعديل 3: ترتيب هرمي واضح للقرار
        values = [
            volatility,     # المخاطرة - الجزء الأكبر
            price_range,    # التقلب
            avg_price,      # القوة
            median_price    # الاستقرار
        ]

        fig = go.Figure(
            data=[
                go.Pie(
                    values=values,
                    hole=0.75,
                    # ✅ ترتيب ألوان يطابق الترتيب الهرمي
                    marker=dict(
                        colors=[
                            self.COLORS["plum"],      # مخاطرة
                            self.COLORS["lavender"],  # تقلب
                            self.COLORS["emerald"],   # قوة
                            self.COLORS["gold"]       # استقرار
                        ],
                        line=dict(width=2, color='white')
                    ),
                    textinfo="none",
                    hoverinfo="none",
                    sort=False
                )
            ]
        )

        fig.update_layout(
            title="الملخص التنفيذي",
            showlegend=False,
            height=520,
            margin=dict(l=20, r=20, t=80, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            font=dict(family="Tajawal"),
            annotations=[]
        )

        fig.update_xaxes(visible=False, showgrid=False, zeroline=False)
        fig.update_yaxes(visible=False, showgrid=False, zeroline=False)

        return fig

    # =====================
    # CHAPTER 8 – FINAL CURVE
    # =====================
    def ch8_final_curve(self, df):
        """
        رسم 8: المنحنى الختامي - نظرة نهائية
        """
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
            title="المنحنى الختامي",
            xaxis_title="نطاق السعر",
            # ✅ التعديل 4: محور Y بدون عنوان أكاديمي
            yaxis_title="",
        )
        
        fig.update_xaxes(tickformat="~s", showgrid=False)
        fig.update_yaxes(showticklabels=False, showgrid=False)
        
        return self._safe(fig, height=520)

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        """
        ✅ المحرك النهائي - رسم واحد واضح لكل فصل
        """
        if df is None or df.empty:
            return {}

        df = self._ensure_numeric_core(df)

        def clean(lst):
            return [x for x in lst if x is not None]

        return {
            # ✅ فصل 1: سعر المتر حسب المنطقة
            "chapter_1": clean([
                self.ch1_price_per_sqm_by_district(df),
            ]),

            # ✅ فصل 2: تدفق الأسعار عبر الزمن
            "chapter_2": clean([
                self.ch2_price_stream(df),
            ]),

            # ✅ فصل 3: توزيع الأسعار
            "chapter_3": clean([
                self.rhythm_price_curve(df, "توزيع الأسعار"),
            ]),

            # ✅ فصل 4: العلاقة بين المساحة والسعر
            "chapter_4": clean([
                self.ch1_price_vs_area_flow(df),
            ]),

            # ✅ فصل 5: لوحة قراءة السوق
            "chapter_5": clean([
                self.ch4_market_indicators_bar(df),
            ]),

            # ✅ فصل 6: مؤشر القرار التنفيذي
            "chapter_6": clean([
                self.ch6_gauge(df),
            ]),

            # ✅ فصل 7: الملخص التنفيذي
            "chapter_7": clean([
                self.ch7_executive_donut(df),
            ]),

            # ✅ فصل 8: المنحنى الختامي
            "chapter_8": clean([
                self.ch8_final_curve(df),
            ]),

            # ❌ الفصول الإضافية فارغة (لنصوص الذكاء الاصطناعي)
            "chapter_9": [],
            "chapter_10": [],
        }!*
