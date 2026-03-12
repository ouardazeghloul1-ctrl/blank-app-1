# advanced_charts.py - الإصدار النهائي المعدّل مع تحسينات بصرية
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from decision_terminology import TERMS


class AdvancedCharts:
    """
    PREMIUM EXECUTIVE CHARTS ENGINE
    مستوى عالمي – هادئ – انسيابي
    
    DATA CONTRACT (FINAL):
    price | area | district | date
    لا يدعم إلا DATA CONTRACT بعد التوحيد
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
    # DECISION CONSTANTS
    # =====================
    DECISION_BASE_PRICE_PER_SQM = 20000  # قاعدة القرار التنفيذي
    LOWER_DECISION_BOUND = 0.9  # الحد الأدنى للنطاق المرجعي
    UPPER_DECISION_BOUND = 1.1  # الحد الأعلى للنطاق المرجعي

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return df is not None and all(col in df.columns for col in cols)

    def _numeric(self, s):
        return pd.to_numeric(s, errors="coerce")
    
    def _remove_outliers(self, df, column, quantile=0.99):
        """
        إزالة القيم المتطرفة (أعلى quantile)
        """
        if df is None or df.empty or column not in df.columns:
            return df
        
        df = df.copy()
        threshold = df[column].quantile(quantile)
        return df[df[column] < threshold]

    def _normalize_market_columns(self, df):
        """
        توحيد أعمدة market_data_core مع محرك الرسومات - نسخة مضمونة 100%
        مع إزالة الأعمدة المكررة
        """
        if df is None or df.empty:
            return df

        df = df.copy()
        df.columns = df.columns.str.strip()

        column_map = {
            "السعر": "price",
            "سعر الصفقة": "price",
            "قيمة الصفقة": "price",

            "المساحة": "area",
            "المساحة م2": "area",

            "الحي": "district",
            "اسم الحي": "district",
            "الحي / المدينة": "district",

            "تاريخ الصفقة": "date",
            "تاريخ البيع": "date",
            "تاريخ التسجيل": "date",
        }

        # إعادة التسمية
        df = df.rename(columns=column_map)

        # إزالة الأعمدة المكررة بعد إعادة التسمية
        df = df.loc[:, ~df.columns.duplicated()]

        # الاحتفاظ فقط بالعقد النهائي
        required = ["price", "area", "district", "date"]
        existing = [c for c in required if c in df.columns]

        return df[existing]

    def _ensure_numeric_core(self, df):
        """
        توحيد وتنظيف البيانات الأساسية للرسومات
        مع معالجة الفواصل العربية والأرقام
        """
        if df is None or df.empty:
            return pd.DataFrame()
            
        df = df.copy()

        # معالجة عمود السعر - إزالة الفواصل العربية والعادية
        if "price" in df.columns:
            # تحويل إلى نص أولاً
            df["price"] = df["price"].astype(str)
            # إزالة الفواصل
            df["price"] = df["price"].str.replace(",", "", regex=False)
            df["price"] = df["price"].str.replace("٬", "", regex=False)
            # تحويل إلى رقم
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # معالجة عمود المساحة - إزالة الفواصل العربية والعادية
        if "area" in df.columns:
            # تحويل إلى نص أولاً
            df["area"] = df["area"].astype(str)
            # إزالة الفواصل
            df["area"] = df["area"].str.replace(",", "", regex=False)
            df["area"] = df["area"].str.replace("٬", "", regex=False)
            # تحويل إلى رقم
            df["area"] = pd.to_numeric(df["area"], errors="coerce")

        # ✅ التاريخ ميلادي من وزارة العدل - نحتفظ به كنص ثم نحوله عند التحليل الزمني
        if "date" in df.columns:
            df["date"] = df["date"].astype(str)

        # إزالة القيم المتطرفة من السعر (أعلى 1%)
        df = self._remove_outliers(df, "price", 0.99)

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
            margin=dict(l=70, r=70, t=90, b=90),  # مسافة موحدة للجميع
            font=dict(size=15, color=self.COLORS["text"], family="Tajawal"),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(tickfont=dict(size=16)),
            title=dict(
                x=0.5,
                font=dict(size=18, color=self.COLORS["text"], family="Tajawal"),
            ),
            plot_bgcolor=self.COLORS["light_gray"],
            paper_bgcolor="white",
            hovermode="closest",
            hoverlabel=dict(font_size=15, font_family="Tajawal"),
        )

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False)

        return fig

    def _executive_caption(self, condition, positive, neutral, negative):
        """
        مولد قراءة تنفيذية ديناميكية - نبرة موحدة لجميع الباقات
        """
        if condition == "positive":
            return positive
        elif condition == "negative":
            return negative
        else:
            return neutral

    def _get_decision_state(self, ratio):
        """
        تحديد حالة القرار بناءً على النسبة من القيمة المرجعية
        """
        if ratio < self.LOWER_DECISION_BOUND:
            return "positive"
        elif ratio > self.UPPER_DECISION_BOUND:
            return "negative"
        else:
            return "neutral"

    # =====================
    # CHAPTER 1 – PRICE PER SQM BY DISTRICT
    # =====================
    def ch1_price_per_sqm_by_district(self, df):
        """
        رسم 1: متوسط سعر المتر حسب المنطقة
        """
        district_col = "district" if "district" in df.columns else None

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

        # إضافة القراءة التنفيذية
        max_price = agg.max() if not agg.empty else 0
        decision_ratio = max_price / self.DECISION_BASE_PRICE_PER_SQM
        state = self._get_decision_state(decision_ratio)

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: مناطق بأسعار أقل من المرجع، تدعم الانتقاء المرحلي.",
            neutral=f"{TERMS['DECISION']['label']}: أسعار ضمن النطاق المرجعي، التحرك مشروط بالتميز.",
            negative=f"{TERMS['DECISION']['label']}: مناطق تتجاوز المرجع، تتطلب انتقاءً أشد."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )

        return self._safe(fig, height=540)

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
        # ✅ التاريخ ميلادي من وزارة العدل - نحتفظ به كنص ثم نحوله عند التحليل الزمني
        tmp["date"] = tmp["date"].astype(str)
        tmp["price"] = self._numeric(tmp["price"])
        tmp = tmp.dropna(subset=["date", "price"])
        tmp = tmp.sort_values("date")  # الترتيب صحيح لأن التاريخ نصي

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

        # إضافة القراءة التنفيذية
        if len(tmp) > 1:
            first_price = tmp["price"].iloc[0]
            last_price = tmp["price"].iloc[-1]
            trend = (last_price - first_price) / first_price if first_price > 0 else 0
            
            if trend > 0.05:
                state = "positive"
            elif trend < -0.05:
                state = "negative"
            else:
                state = "neutral"
        else:
            state = "neutral"

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: اتجاه صاعد يدعم الاستراتيجية طويلة المدى.",
            neutral=f"{TERMS['DECISION']['label']}: استقرار اتجاهي، التحرك وفق {TERMS['PROTOCOL']['label']}.",
            negative=f"{TERMS['DECISION']['label']}: اتجاه هابط يتطلب حذراً وانتقاءً أشد."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )

        return self._safe(fig, height=540)

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
            annotation_text="متوسط السعر",
            annotation_position="top",
            annotation_font=dict(size=12, family="Tajawal")
        )

        fig.update_layout(title=title)
        fig.update_xaxes(tickformat="~s")

        # تحديد نطاق المحور X لتحسين المظهر
        price_threshold = p.quantile(0.99)
        fig.update_xaxes(range=[0, price_threshold])

        # إضافة القراءة التنفيذية
        mean_price = p.mean()
        decision_ratio = mean_price / self.DECISION_BASE_PRICE_PER_SQM
        state = self._get_decision_state(decision_ratio)

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: التسعير دون المستوى المرجعي، الانتقاء المرحلي مدعوم.",
            neutral=f"{TERMS['DECISION']['label']}: السوق ضمن النطاق المرجعي، التحرك مشروط بالتميز.",
            negative=f"{TERMS['DECISION']['label']}: التسعير أعلى من المرجع، لا يدعم توسعاً أفقيًا."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )

        return self._safe(fig, height=540)

    # =====================
    # CHAPTER 4 – MARKET RELATION
    # =====================
    def ch4_price_vs_area_flow(self, df):
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

        # تحديد نطاق المحور Y لتحسين المظهر
        price_threshold = tmp["price"].quantile(0.99)
        fig.update_yaxes(range=[0, price_threshold])

        # إضافة القراءة التنفيذية
        avg_price_per_sqm = (tmp["price"] / tmp["area"]).mean()
        decision_ratio = avg_price_per_sqm / self.DECISION_BASE_PRICE_PER_SQM
        state = self._get_decision_state(decision_ratio)

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: العلاقة السعر-مساحة تدعم الانتقاء الانتقائي.",
            neutral=f"{TERMS['DECISION']['label']}: العلاقة ضمن النطاق، التحرك مشروط بالميزة.",
            negative=f"{TERMS['DECISION']['label']}: العلاقة تتجاوز المرجع، تتطلب انتقاءً أشد."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )

        return self._safe(fig, height=540)

    # =====================
    # CHAPTER 5 – MARKET INDICATORS
    # =====================
    def ch5_market_indicators_bar(self, df):
        """
        رسم 5: لوحة قراءة السوق
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

        # إضافة القراءة التنفيذية
        decision_ratio = price_per_sqm / self.DECISION_BASE_PRICE_PER_SQM if price_per_sqm > 0 else 1
        state = self._get_decision_state(decision_ratio)

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: المؤشرات تدعم تفعيل استراتيجية الانتقاء المرحلي.",
            neutral=f"{TERMS['DECISION']['label']}: المؤشرات متوازنة، الالتزام بـ {TERMS['PROTOCOL']['label']}.",
            negative=f"{TERMS['DECISION']['label']}: المؤشرات تتطلب انتقاءً أشد، لا توسع أفقي."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )

        return self._safe(fig, height=540)

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
            score = min(100, max(0, (price_per_sqm / self.DECISION_BASE_PRICE_PER_SQM) * 100))
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
            title=TERMS['DCI']['label'],
            height=540,
            margin=dict(l=30, r=30, t=90, b=90),
            font=dict(family="Tajawal", size=18)
        )

        # إضافة القراءة التنفيذية
        if score >= 70:
            state = "positive"
        elif score <= 40:
            state = "negative"
        else:
            state = "neutral"

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: {TERMS['DCI']['display']} مرتفع يدعم التحرك المنضبط وفق {TERMS['PROTOCOL']['label']}.",
            neutral=f"{TERMS['DECISION']['label']}: {TERMS['DCI']['display']} متوسط، يتطلب انتقاءً صارماً دون توسع.",
            negative=f"{TERMS['DECISION']['label']}: {TERMS['DCI']['display']} منخفض، البيئة الحالية تتطلب حذراً وانتقاءً أشد."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )

        return self._safe(fig, height=540)

    # =====================
    # CHAPTER 7 – EXECUTIVE DECISION BAR
    # =====================
    def ch7_executive_decision_bar(self, df):
        """
        رسم 7: قرار الاستثمار التنفيذي (بديل Donut الملخص التنفيذي)
        """
        if not self._has_columns(df, ["price", "area"]):
            return None

        tmp = df.copy()
        tmp["price"] = self._numeric(tmp["price"])
        tmp["area"] = self._numeric(tmp["area"])
        tmp = tmp.dropna(subset=["price", "area"])

        if len(tmp) < 5:
            return None

        price_per_sqm = (tmp["price"] / tmp["area"]).mean()

        # تحويله إلى مقياس قرار (0 – 100)
        score = min(100, max(0, (price_per_sqm / self.DECISION_BASE_PRICE_PER_SQM) * 100))

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=[score],
                y=[TERMS['DECISION']['label']],
                orientation="h",
                marker=dict(color=self.COLORS["emerald"]),
                text=[f"{score:.0f}"],
                textposition="outside"
            )
        )

        fig.update_layout(
            title=TERMS['DECISION']['label'],
            xaxis=dict(
                range=[0, 100],
                visible=False
            ),
            yaxis=dict(
                visible=False
            ),
            showlegend=False,
            height=360,
            margin=dict(l=70, r=70, t=90, b=90),
            font=dict(family="Tajawal")
        )

        # إضافة القراءة التنفيذية
        if score >= 70:
            state = "positive"
        elif score <= 40:
            state = "negative"
        else:
            state = "neutral"

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: درجة قرار عالية، تفعيل الاستراتيجية طويل المدى.",
            neutral=f"{TERMS['DECISION']['label']}: درجة قرار متوسطة، {TERMS['PROTOCOL']['label']} صارم.",
            negative=f"{TERMS['DECISION']['label']}: درجة قرار منخفضة، تعليق أي توسع أفقي."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )

        return self._safe(fig, height=400)

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
            yaxis_title="",
        )
        
        fig.update_xaxes(tickformat="~s", showgrid=False)
        fig.update_yaxes(showticklabels=False, showgrid=False)

        # تحديد نطاق المحور X لتحسين المظهر
        price_threshold = p.quantile(0.99)
        fig.update_xaxes(range=[0, price_threshold])

        # إضافة القراءة التنفيذية
        mean_price = p.mean()
        decision_ratio = mean_price / self.DECISION_BASE_PRICE_PER_SQM
        state = self._get_decision_state(decision_ratio)

        caption = self._executive_caption(
            state,
            positive=f"{TERMS['DECISION']['label']}: المؤشرات الختامية تؤكد صلاحية {TERMS['DECISION']['label']}.",
            neutral=f"{TERMS['DECISION']['label']}: المؤشرات الختامية متوازنة، لا تعديل على {TERMS['DECISION']['label']}.",
            negative=f"{TERMS['DECISION']['label']}: المؤشرات الختامية تحذّر، استمرار الانضباط."
        )

        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.18,
            showarrow=False,
            font=dict(size=14, family="Tajawal", color=self.COLORS["text"]),
            align="center"
        )
        
        return self._safe(fig, height=540)

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        """
        ✅ المحرك النهائي - رسم واحد واضح لكل فصل
        متوافق مع بيانات وزارة العدل
        """
        if df is None or df.empty:
            return {}

        # ✅ توحيد الأعمدة أولاً - يرجع إنجليزي فقط (متوافق مع وزارة العدل)
        df = self._normalize_market_columns(df)
        df = self._ensure_numeric_core(df)

        def clean(lst):
            return [x for x in lst if x is not None]

        return {
            # ✅ فصل 1: سعر المتر حسب المنطقة
            "chapter_1": clean([
                self.ch1_price_per_sqm_by_district(df),
            ]),

            # ✅ فصل 2: تدفق الأسعار عبر الزمن (يعمل مع التاريخ الميلادي)
            "chapter_2": clean([
                self.ch2_price_stream(df),
            ]),

            # ✅ فصل 3: توزيع الأسعار
            "chapter_3": clean([
                self.rhythm_price_curve(df, "توزيع الأسعار"),
            ]),

            # ✅ فصل 4: العلاقة بين المساحة والسعر
            "chapter_4": clean([
                self.ch4_price_vs_area_flow(df),
            ]),

            # ✅ فصل 5: لوحة قراءة السوق
            "chapter_5": clean([
                self.ch5_market_indicators_bar(df),
            ]),

            # ✅ فصل 6: مؤشر القرار التنفيذي
            "chapter_6": clean([
                self.ch6_gauge(df),
            ]),

            # ✅ فصل 7: قرار الاستثمار التنفيذي
            "chapter_7": clean([
                self.ch7_executive_decision_bar(df),
            ]),

            # ✅ فصل 8: المنحنى الختامي
            "chapter_8": clean([
                self.ch8_final_curve(df),
            ]),

            # ❌ الفصول الإضافية فارغة (لنصوص الذكاء الاصطناعي)
            "chapter_9": [],
            "chapter_10": [],
        }

    # =====================
    # DISTRICT PRICE TREND
    # =====================
    def generate_district_price_trend(self, df, district):
        """
        تطور سعر المتر في حي معين عبر الزمن
        """
        if df is None or df.empty:
            return None

        if not self._has_columns(df, ["price", "area", "district", "date"]):
            return None

        df = df.copy()

        # فلترة الحي
        df = df[df["district"] == district]

        if df.empty:
            return None

        # حساب سعر المتر مع التأكد من عدم وجود مساحة صفرية
        df = df[df["area"] > 0]
        if df.empty:
            return None
            
        df["price_per_sqm"] = df["price"] / df["area"]

        # تحويل التاريخ (التاريخ ميلادي)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        # تجميع شهري
        df["month"] = df["date"].dt.to_period("M").astype(str)

        monthly = (
            df.groupby("month")["price_per_sqm"]
            .mean()
            .reset_index()
            .sort_values("month")  # ترتيب الأشهر
        )

        if monthly.empty:
            return None

        fig = px.line(
            monthly,
            x="month",
            y="price_per_sqm",
            title=f"تطور سعر المتر في حي {district}",
            markers=True,
            color_discrete_sequence=[self.COLORS["emerald"]],
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="التاريخ",
            yaxis_title="سعر المتر",
            font=dict(family="Tajawal"),
        )

        return fig

    # =====================
    # DISTRICT COMPARISON
    # =====================
    def generate_district_comparison(self, df, districts=None):
        """
        مقارنة أسعار الأحياء
        """
        if df is None or df.empty:
            return None

        if not self._has_columns(df, ["price", "area", "district"]):
            return None

        df = df.copy()
        
        # حساب سعر المتر مع التأكد من عدم وجود مساحة صفرية
        df = df[df["area"] > 0]
        if df.empty:
            return None
            
        df["price_per_sqm"] = df["price"] / df["area"]

        # إذا لم يتم تحديد أحياء، نأخذ أشهر 5 أحياء
        if districts is None:
            districts = df["district"].value_counts().head(5).index.tolist()

        df = df[df["district"].isin(districts)]

        if df.empty:
            return None

        comparison = (
            df.groupby("district")["price_per_sqm"]
            .mean()
            .reset_index()
            .sort_values("price_per_sqm", ascending=False)
        )

        fig = px.bar(
            comparison,
            x="district",
            y="price_per_sqm",
            title="مقارنة متوسط سعر المتر بين الأحياء",
            color="district",
            color_discrete_sequence=[self.COLORS["emerald"], self.COLORS["gold"], self.COLORS["plum"], self.COLORS["mint"], self.COLORS["lavender"]],
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="الحي",
            yaxis_title="متوسط سعر المتر",
            showlegend=False,
            font=dict(family="Tajawal"),
        )

        return fig

    # =====================
    # DISTRICT TRANSACTIONS OVER TIME
    # =====================
    def generate_district_transactions_over_time(self, df, district):
        """
        عدد الصفقات في الحي عبر الزمن
        """
        if df is None or df.empty:
            return None

        if not self._has_columns(df, ["district", "date"]):
            return None

        df = df.copy()
        df = df[df["district"] == district]

        if df.empty:
            return None

        # تحويل التاريخ (التاريخ ميلادي)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        df["month"] = df["date"].dt.to_period("M").astype(str)

        monthly = (
            df.groupby("month")
            .size()
            .reset_index(name="transactions")
            .sort_values("month")  # ترتيب الأشهر
        )

        if monthly.empty:
            return None

        fig = px.bar(
            monthly,
            x="month",
            y="transactions",
            title=f"عدد الصفقات عبر الزمن في حي {district}",
            color_discrete_sequence=[self.COLORS["emerald"]],
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="الشهر",
            yaxis_title="عدد الصفقات",
            font=dict(family="Tajawal"),
        )

        return fig

    # =====================
    # DISTRICT PRICE DISTRIBUTION
    # =====================
    def generate_district_price_distribution(self, df, district):
        """
        توزيع الأسعار داخل الحي
        """
        if df is None or df.empty:
            return None

        if "price" not in df.columns or "district" not in df.columns:
            return None

        df = df.copy()
        df = df[df["district"] == district]

        if df.empty:
            return None

        prices = pd.to_numeric(df["price"], errors="coerce").dropna()

        if len(prices) < 5:
            return None

        fig = px.histogram(
            prices,
            nbins=30,
            title=f"توزيع الأسعار في حي {district}",
            color_discrete_sequence=[self.COLORS["plum"]],
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="السعر",
            yaxis_title="عدد الصفقات",
            font=dict(family="Tajawal"),
        )

        # تحديد نطاق المحور X لتحسين المظهر
        price_threshold = prices.quantile(0.99)
        fig.update_xaxes(range=[0, price_threshold])

        return fig

    # =====================
    # DISTRICT PROPERTY TYPE ANALYSIS
    # =====================
    def generate_district_property_type_analysis(self, df, district):
        """
        تحليل أنواع العقارات في الحي
        """
        if df is None or df.empty:
            return None

        if not self._has_columns(df, ["district", "property_type"]):
            return None

        df = df.copy()
        df = df[df["district"] == district]

        if df.empty:
            return None

        analysis = (
            df.groupby("property_type")
            .size()
            .reset_index(name="transactions")
        )

        fig = px.pie(
            analysis,
            names="property_type",
            values="transactions",
            title=f"توزيع أنواع العقارات في حي {district}",
            color_discrete_sequence=[
                self.COLORS["emerald"],
                self.COLORS["gold"],
                self.COLORS["plum"],
            ],
        )

        fig.update_layout(
            template="plotly_white",
            font=dict(family="Tajawal"),
        )

        # تحديث تنسيق النص في الـ pie chart
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(family="Tajawal", size=14)
        )

        return fig

    # =====================
    # DISTRICT CHARTS ENGINE
    # =====================
    def generate_all_district_charts(self, df, district, nearby_districts=None):
        """
        محرك توليد جميع رسومات الحي
        يعيد قاموس يحتوي على كل الرسومات الجاهزة للاستخدام في PDF أو الواجهة
        """
        if df is None or df.empty:
            return {}

        # توحيد الأعمدة أولاً
        df = self._normalize_market_columns(df)
        df = self._ensure_numeric_core(df)

        charts = {}

        # 1️⃣ تطور سعر المتر
        price_trend = self.generate_district_price_trend(df, district)
        if price_trend is not None:
            charts["price_trend"] = price_trend

        # 2️⃣ مقارنة الأحياء
        comparison = self.generate_district_comparison(df, nearby_districts)
        if comparison is not None:
            charts["district_comparison"] = comparison

        # 3️⃣ عدد الصفقات عبر الزمن
        transactions = self.generate_district_transactions_over_time(df, district)
        if transactions is not None:
            charts["transactions_over_time"] = transactions

        # 4️⃣ توزيع الأسعار
        distribution = self.generate_district_price_distribution(df, district)
        if distribution is not None:
            charts["price_distribution"] = distribution

        # 5️⃣ تحليل أنواع العقارات
        property_types = self.generate_district_property_type_analysis(df, district)
        if property_types is not None:
            charts["property_type_analysis"] = property_types

        return charts
