# advanced_charts.py - الإصدار النهائي النخبوي
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
    # DONUT HELPER (التنظيم المحسّن)
    # =====================
    def _donut_base_layout(self, fig, title):
        """
        ✅ Helper موحد لإعدادات الدونت الأساسية
        """
        fig.update_layout(
            showlegend=False,
            title=dict(
                text=title,
                font=dict(size=24, family="Tajawal", color=self.COLORS["text"]),
                y=0.97,
                x=0.5,
                xanchor="center",
                pad=dict(t=10, b=10)
            ),
            margin=dict(l=20, r=120, t=80, b=60),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            height=520,
            font=dict(family="Tajawal"),
            annotations=[]
        )

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
            "hole": 0.85,
            "domain": dict(x=[0.05, 0.95], y=[0.10, 0.90]),
            "marker": dict(
                colors=colors,
                line=dict(width=2, color='white')
            ),
            "textinfo": "none",
            "hoverinfo": "none",
            "direction": 'clockwise',
            "rotation": 90,
            "sort": False
        }

    # =====================
    # REAL DATA – PRICE PER SQM BY DISTRICT
    # =====================
    def ch1_price_per_sqm_by_district(self, df):
        """
        رسم حقيقي: متوسط سعر المتر حسب المنطقة
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
    # RHYTHM 1 – DONUT INSIGHT
    # =====================
    def rhythm_price_donut(self, df, title=None):
        """
        ✅ الإصدار النهائي - مع Legend يدوي احترافي
        """
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 5:
            return None

        low = (p < p.quantile(0.33)).sum()
        mid = ((p >= p.quantile(0.33)) & (p < p.quantile(0.66))).sum()
        high = (p >= p.quantile(0.66)).sum()

        total = low + mid + high
        if total == 0:
            return None

        low_pct = round((low / total) * 100)
        mid_pct = round((mid / total) * 100)
        high_pct = round((high / total) * 100)

        fig = go.Figure(
            data=[
                go.Pie(
                    values=[low, mid, high],
                    **self._donut_base_style()
                )
            ]
        )

        fig = self._donut_base_layout(
            fig,
            title or "توزيع مستويات الأسعار"
        )

        # =====================
        # CUSTOM LEGEND (RIGHT SIDE) - صيغة RTL ثابتة
        # =====================

        legend_items = [
            {
                "label": f"أسعار منخفضة — نسبة {low_pct}",
                "color": self.COLORS["mint"],
                "y": 0.60
            },
            {
                "label": f"أسعار متوسطة — نسبة {mid_pct}",
                "color": self.COLORS["lavender"],
                "y": 0.50
            },
            {
                "label": f"أسعار مرتفعة — نسبة {high_pct}",
                "color": self.COLORS["gold"],
                "y": 0.40
            },
        ]

        for item in legend_items:
            fig.add_shape(
                type="rect",
                xref="paper",
                yref="paper",
                x0=1.01,
                x1=1.04,
                y0=item["y"] - 0.015,
                y1=item["y"] + 0.015,
                fillcolor=item["color"],
                line=dict(width=0)
            )

            fig.add_annotation(
                x=1.05,
                y=item["y"],
                xref="paper",
                yref="paper",
                text=item["label"],
                showarrow=False,
                align="left",
                font=dict(
                    size=14,
                    family="Tajawal",
                    color=self.COLORS["text"]
                )
            )

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
            annotation_text=f"متوسط السوق {p.mean():,.0f}",
            annotation_position="top",
            annotation_font=dict(size=12, family="Tajawal")
        )

        fig.update_layout(title=title)
        return self._safe(fig, height=520)

    # =====================
    # CHAPTER 1 – MARKET RELATION
    # =====================
    def ch1_price_vs_area_flow(self, df):
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
                # ✅ Hover Text مختصر ونظيف
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
    # CHAPTER 2 – TIME FLOW
    # =====================
    def ch2_price_stream(self, df):
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
    # CHAPTER 3 – SAMPLE TABLE
    # =====================
    def ch3_table_sample(self, df):
        if not self._has_columns(df, ["price", "area"]):
            return None

        sample_size = min(12, len(df))
        if sample_size < 3:
            return None
            
        sample = df[["area", "price"]].sample(n=sample_size, random_state=42)

        sample_display = sample.copy()
        sample_display["price"] = sample_display["price"].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "")
        sample_display["area"] = sample_display["area"].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "")

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["المساحة م²", "السعر"],
                        fill_color="#F4F6F8",
                        align="center",
                        font=dict(
                            size=14,
                            color="#1F2933",
                            family="Tajawal"
                        ),
                    ),
                    cells=dict(
                        values=[sample_display["area"], sample_display["price"]],
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

        fig.update_layout(
            title=f"عينة ذكية من بيانات السوق {sample_size} عقار",
            height=560
        )
        return fig

    # =====================
    # CHAPTER 4 – MARKET INDICATORS BAR
    # =====================
    def ch4_market_indicators_bar(self, df):
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
        
        # ✅ قيمة صادقة تحليليًا (بدل التحديد الاصطناعي بـ 100)
        values = [
            (avg_price / 3000000) * 100,
            (avg_area / 200) * 100,
            (price_per_sqm / 15000) * 100
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
                text=[f"{v:.0f} بالمئة" for v in values],
                textposition="outside"
            )
        )

        # ✅ نطاق ديناميكي بناءً على القيم الحقيقية
        max_value = max(values) if values else 100
        x_range = [0, max_value * 1.1]

        fig.update_layout(
            title="مقارنة مؤشرات السوق الرئيسية",
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
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 3:
            return None

        lower = p.quantile(0.25)
        middle_lower = p.quantile(0.5) - p.quantile(0.25)
        middle_upper = p.quantile(0.75) - p.quantile(0.5)
        upper = p.max() - p.quantile(0.75)

        # ✅ ترتيب هرمي واضح
        values = [
            upper,          # القرار الأقوى
            middle_upper,   # قرار داعم
            middle_lower,   # قرار ثانوي
            lower           # هامشي
        ]

        fig = go.Figure(
            data=[
                go.Pie(
                    values=values,
                    **self._donut_base_style([
                        self.COLORS["gold"],
                        self.COLORS["plum"],
                        self.COLORS["mint"],
                        self.COLORS["emerald"]
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
    # CHAPTER 8 – FINAL CURVE
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
            title="المنحنى الختامي",
            xaxis_title="نطاق السعر",
            yaxis_title="الكثافة النسبية",
        )
        
        # ✅ تنسيق القيم لقراءة تنفيذية
        fig.update_xaxes(tickformat="~s")
        
        return self._safe(fig, height=520)

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        """
        ✅ المحرك النهائي - توزيع الرسومات على الفصول
        """
        if df is None or df.empty:
            return {}

        df = self._ensure_numeric_core(df)

        def clean(lst):
            return [x for x in lst if x is not None]

        return {
            "chapter_1": clean([
                self.ch1_price_per_sqm_by_district(df),
                self.ch1_price_vs_area_flow(df),
                self.rhythm_price_curve(df, "توزيع الأسعار بانسيابية"),
            ]),
            "chapter_2": clean([
                self.ch2_price_stream(df),
                self.rhythm_price_donut(df, "مستويات الأسعار"),
                self.rhythm_price_curve(df, "توزيع الأسعار عبر الزمن"),
            ]),
            "chapter_3": clean([
                self.ch3_table_sample(df),
                self.rhythm_price_donut(df, "نطاق العينة"),
                self.rhythm_price_curve(df, "تشتت الأسعار"),
            ]),
            "chapter_4": clean([
                self.rhythm_price_donut(df, "نطاقات السوق"),
                self.ch4_market_indicators_bar(df),
            ]),
            # ✅ الفصل الخامس: رسم واحد فقط
            "chapter_5": clean([
                self.rhythm_price_donut(df, "قراءة هيكلية للسوق"),
            ]),
            # ✅ الفصل السادس: Donut + Gauge فقط
            "chapter_6": clean([
                self.rhythm_price_donut(df, "رأس المال"),
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
