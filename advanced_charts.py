# advanced_charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class AdvancedCharts:
    """
    PREMIUM EXECUTIVE CHARTS ENGINE
    مستوى عالمي – هادئ – انسيابي
    تقرير عقاري تنفيذي رقم واحد في السعودية
    """

    # =====================
    # VISUAL IDENTITY
    # =====================
    COLORS = {
        "primary": "#1B5E20",        # زمردي (لون رئيسي)
        "secondary": "#6A1B9A",      # بنفسجي (لون ثانوي)
        "accent": "#C9A227",         # ذهبي (لون إبراز)
        "light": "#A5D6A7",          # أخضر فاتح
        "pale": "#E1BEE7",           # بنفسجي فاتح
        "background": "#F5F5F5",     # خلفية فاتحة
        "text": "#333333",           # نص داكن
        "white": "#FFFFFF",          # أبيض
    }

    # =====================
    # HELPERS
    # =====================
    def _has_columns(self, df, cols):
        return df is not None and all(col in df.columns for col in cols)

    def _numeric(self, s):
        return pd.to_numeric(s, errors="coerce")

    def _safe(self, fig, height=550, is_executive=False):
        """تخطيط قاعدي متقدم مع هوية بصرية موحدة"""
        if fig is None:
            return None

        # تحديد الارتفاع بناءً على نوع الرسم
        if is_executive:
            height = 650  # الرسومات التنفيذية أكبر

        fig.update_layout(
            template="plotly_white",
            height=height,
            margin=dict(l=50, r=50, t=100, b=50),
            font=dict(
                size=14,
                color=self.COLORS["text"],
                family="Tajawal, Arial, sans-serif"
            ),
            title=dict(
                x=0.5,
                font=dict(size=20, color=self.COLORS["primary"]),
                y=0.95
            ),
            plot_bgcolor=self.COLORS["background"],  # تغيير: خلفية الرسم بلون فاتح
            paper_bgcolor=self.COLORS["white"],      # خلفية الورق بيضاء
            hovermode="x unified",
            showlegend=False,
        )

        # إعدادات محور X
        fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            linecolor="rgba(0,0,0,0.1)",
            tickfont=dict(size=12)
        )
        
        # إعدادات محور Y
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False,
            linecolor="rgba(0,0,0,0.1)",
            tickfont=dict(size=12)
        )

        return fig

    # =====================
    # CHAPTER 1 – فهم السوق
    # =====================
    def ch1_scatter_flow(self, df):
        """مخطط تبعثر انسيابي للسعر مقابل المساحة"""
        if not self._has_columns(df, ["price", "area"]):
            return None

        df = df.copy()
        df["price"] = self._numeric(df["price"])
        df["area"] = self._numeric(df["area"])
        df = df.dropna()

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["area"],
                y=df["price"],
                mode="markers",
                marker=dict(
                    size=12,
                    color=self.COLORS["primary"],
                    opacity=0.6,
                    line=dict(width=1, color="white")
                ),
                name="عقارات",
                hovertemplate="المساحة: %{x:,.0f} م²<br>السعر: %{y:,.0f} ريال<br><extra></extra>"
            )
        )

        # خط الاتجاه
        if len(df) > 1:
            z = np.polyfit(df["area"], df["price"], 1)
            p = np.poly1d(z)
            fig.add_trace(
                go.Scatter(
                    x=df["area"],
                    y=p(df["area"]),
                    mode="lines",
                    line=dict(color=self.COLORS["accent"], width=2, dash="dash"),
                    name="اتجاه السوق"
                )
            )

        fig.update_layout(
            title="تحليل العلاقة بين المساحة والسعر",
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر (ريال)",
            showlegend=True
        )

        fig = self._safe(fig, height=600)
        # إخفاء الشبكة للمخططات الكبيرة (اختياري)
        fig.update_yaxes(showgrid=False)
        return fig

    def ch1_price_distribution(self, df):
        """توزيع الأسعار بانسيابية"""
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 10:
            return None

        # حساب الكثافة
        hist_y, hist_x = np.histogram(p, bins=30, density=True)
        hist_x = (hist_x[:-1] + hist_x[1:]) / 2

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hist_x,
                y=hist_y,
                mode="lines",
                line=dict(color=self.COLORS["secondary"], width=3),
                fill="tozeroy",
                fillcolor="rgba(106,27,154,0.15)",
                name="كثافة الأسعار",
                smooth=True  # إضافة: تخطيط ناعم
            )
        )

        # إضافة مؤشرات مهمة
        indicators = [
            (p.quantile(0.25), "25%", self.COLORS["light"]),
            (p.median(), "الوسيط", self.COLORS["primary"]),
            (p.quantile(0.75), "75%", self.COLORS["accent"]),
        ]

        for value, label, color in indicators:
            fig.add_vline(
                x=value,
                line=dict(color=color, width=2, dash="dot"),
                annotation_text=label,
                annotation_position="top",
                annotation_font=dict(size=12)
            )

        fig.update_layout(
            title="توزيع الأسعار في السوق",
            xaxis_title="السعر (ريال)",
            yaxis_title="الكثافة",
        )

        return self._safe(fig, height=500)

    def ch1_market_overview(self, df):
        """نظرة عامة على السوق"""
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if p.empty:
            return None

        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=p.mean(),
                number=dict(
                    prefix="﷼ ",
                    font=dict(size=48, color=self.COLORS["primary"])
                ),
                delta=dict(
                    reference=p.median(),
                    relative=True,
                    font=dict(size=20)
                ),
                title=dict(
                    text="متوسط السوق",
                    font=dict(size=24, color=self.COLORS["text"])
                ),
                domain={'x': [0, 1], 'y': [0.6, 1]}
            )
        )

        fig.add_trace(
            go.Indicator(
                mode="number",
                value=len(p),
                number=dict(
                    font=dict(size=36, color=self.COLORS["secondary"])
                ),
                title=dict(
                    text="عدد العقارات",
                    font=dict(size=18, color=self.COLORS["text"])
                ),
                domain={'x': [0, 0.5], 'y': [0, 0.4]}
            )
        )

        fig.add_trace(
            go.Indicator(
                mode="number",
                value=p.std() / p.mean() * 100 if p.mean() > 0 else 0,
                number=dict(
                    suffix="%",
                    font=dict(size=36, color=self.COLORS["accent"])
                ),
                title=dict(
                    text="معامل التباين",
                    font=dict(size=18, color=self.COLORS["text"])
                ),
                domain={'x': [0.5, 1], 'y': [0, 0.4]}
            )
        )

        fig.update_layout(
            title="نظرة عامة على السوق",
            grid={'rows': 2, 'columns': 2, 'pattern': "independent"}
        )

        # تغيير: زيادة الارتفاع إلى 450 بدلاً من 400
        return self._safe(fig, height=450)

    # =====================
    # CHAPTER 2 – الزمن
    # =====================
    def ch2_price_stream(self, df):
        """تدفق الأسعار عبر الزمن"""
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
                line=dict(color=self.COLORS["primary"], width=3),
                fill="tozeroy",
                fillcolor="rgba(27,94,32,0.1)",
                name="مسار السعر"
            )
        )

        # متوسط متحرك
        if len(df) > 5:
            df['moving_avg'] = df['price'].rolling(window=5, min_periods=1).mean()
            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["moving_avg"],
                    mode="lines",
                    line=dict(color=self.COLORS["accent"], width=2, dash="dash"),
                    name="المتوسط المتحرك (5)"
                )
            )

        fig.update_layout(
            title="تطور الأسعار عبر الزمن",
            xaxis_title="التاريخ",
            yaxis_title="السعر (ريال)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return self._safe(fig, height=550)

    def ch2_area_ribbon(self, df):
        """شريط التدفق الزمني الناعم"""
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
                line=dict(color=self.COLORS["light"], width=1),
                fill="tozeroy",
                fillcolor="rgba(165,214,167,0.2)",
                name="منطقة التداول"
            )
        )

        fig.update_layout(
            title="منطقة التداول الزمنية",
            xaxis_title="التاريخ",
            yaxis_title="السعر (ريال)",
        )

        return self._safe(fig, height=450)

    # =====================
    # CHAPTER 3 – البيانات
    # =====================
    def ch3_data_table(self, df):
        """جدول بيانات نظيف ومقروء"""
        if not self._has_columns(df, ["price", "area", "location"]):
            return None

        sample = df.head(10).copy()
        
        # تنظيف البيانات للعرض
        if "price" in sample.columns:
            sample["price"] = sample["price"].apply(
                lambda x: f"{float(x):,.0f}" if pd.notnull(x) else "N/A"
            )
        
        if "area" in sample.columns:
            sample["area"] = sample["area"].apply(
                lambda x: f"{float(x):,.0f}" if pd.notnull(x) else "N/A"
            )

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["الموقع", "المساحة (م²)", "السعر (ريال)"],
                        fill_color=self.COLORS["background"],
                        align="center",
                        font=dict(size=14, color=self.COLORS["text"], family="Tajawal"),
                        height=40
                    ),
                    cells=dict(
                        values=[
                            sample.get("location", ["N/A"] * len(sample)),
                            sample.get("area", ["N/A"] * len(sample)),
                            sample.get("price", ["N/A"] * len(sample))
                        ],
                        fill_color=[self.COLORS["white"]] * len(sample),
                        align="center",
                        font=dict(size=13, color=self.COLORS["text"], family="Arial"),
                        height=35
                    ),
                    columnwidth=[0.4, 0.3, 0.3]
                )
            ]
        )

        fig.update_layout(
            title="عينة من بيانات السوق",
            margin=dict(l=20, r=20, t=80, b=20)
        )

        return self._safe(fig, height=400)

    def ch3_data_quality(self, df):
        """جودة البيانات ونظافتها"""
        if df is None:
            return None

        stats = {
            "إجمالي السجلات": len(df),
            "بيانات كاملة": df.notnull().all(axis=1).sum(),
            "نسبة الاكتمال": (df.notnull().sum().sum() / (len(df) * len(df.columns))) * 100,
        }

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=list(stats.keys()),
                y=list(stats.values()),
                marker_color=[self.COLORS["primary"], self.COLORS["secondary"], self.COLORS["accent"]],
                text=[f"{v:,}" if isinstance(v, int) else f"{v:.1f}%" for v in stats.values()],
                textposition="outside",
            )
        )

        fig.update_layout(
            title="جودة البيانات",
            yaxis_title="القيمة",
            showlegend=False
        )

        return self._safe(fig, height=400)

    # =====================
    # CHAPTER 4 – التحليل الاستراتيجي
    # =====================
    def ch4_strategic_radar(self, df):
        """رادار تحليلي استراتيجي"""
        if not self._has_columns(df, ["price", "area"]):
            return None

        # حساب المؤشرات الاستراتيجية
        p = self._numeric(df["price"]).dropna()
        a = self._numeric(df["area"]).dropna()

        if p.empty or a.empty:
            return None

        metrics = {
            "الجاذبية السعرية": min(1.0, (p.max() - p.mean()) / p.max()),
            "تنوع المساحات": min(1.0, a.std() / a.mean() if a.mean() > 0 else 0),
            "كثافة السوق": min(1.0, len(p) / 100),  # نسبة افتراضية
            "استقرار الأسعار": min(1.0, 1 - (p.std() / p.mean() if p.mean() > 0 else 0)),
            "قيمة المساحة": min(1.0, (p.mean() / a.mean()) / (p.max() / a.max()) if a.mean() > 0 else 0),
        }

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself',
            fillcolor='rgba(106,27,154,0.15)',
            line=dict(color=self.COLORS["secondary"], width=2),
            name="مؤشرات السوق"
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(size=11)
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            title="الرادار الاستراتيجي للسوق",
            showlegend=False
        )

        return self._safe(fig, height=550)

    # =====================
    # CHAPTER 5 – الفرص
    # =====================
    def ch5_opportunity_bubble(self, df):
        """مخطط الفقاعات للفرص الاستثمارية"""
        if not self._has_columns(df, ["price", "area"]):
            return None

        df = df.copy()
        df["price_num"] = self._numeric(df["price"])
        df["area_num"] = self._numeric(df["area"])
        df = df.dropna()

        if df.empty:
            return None

        # حساب كثافة الفرص (قيمة المساحة)
        df["value_density"] = df["price_num"] / df["area_num"]
        df["size"] = np.sqrt(df["price_num"]) / np.sqrt(df["price_num"].max()) * 40

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["area_num"],
                y=df["price_num"],
                mode='markers',
                marker=dict(
                    size=df["size"],
                    color=df["value_density"],
                    colorscale=[self.COLORS["light"], self.COLORS["primary"]],
                    opacity=0.7,
                    line=dict(width=1, color='white'),
                    colorbar=dict(
                        title="قيمة/م²",
                        thickness=20,
                        len=0.8
                    )
                ),
                text=[f"القيمة/م²: {v:,.0f}" for v in df["value_density"]],
                hoverinfo='text+x+y',
                name="فرص استثمارية"
            )
        )

        fig.update_layout(
            title="خريطة الفرص الاستثمارية",
            xaxis_title="المساحة (م²)",
            yaxis_title="السعر (ريال)",
        )

        fig = self._safe(fig, height=600)
        # إخفاء الشبكة للمخططات الكبيرة (اختياري)
        fig.update_yaxes(showgrid=False)
        return fig

    def ch5_value_distribution(self, df):
        """توزيع القيمة لكل متر مربع"""
        if not self._has_columns(df, ["price", "area"]):
            return None

        df = df.copy()
        df["price"] = self._numeric(df["price"])
        df["area"] = self._numeric(df["area"])
        df = df.dropna()
        
        if df.empty:
            return None

        df["value_per_m2"] = df["price"] / df["area"]

        fig = go.Figure()

        fig.add_trace(
            go.Box(
                y=df["value_per_m2"],
                name="القيمة/م²",
                boxpoints=False,
                marker_color=self.COLORS["accent"],
                line_color=self.COLORS["primary"]
            )
        )

        fig.update_layout(
            title="توزيع القيمة لكل متر مربع",
            yaxis_title="السعر لكل م² (ريال)",
            showlegend=False
        )

        return self._safe(fig, height=450)

    # =====================
    # CHAPTER 6 – القرار
    # =====================
    def ch6_executive_gauge(self, df):
        """مؤشر تنفيذي للقرار"""
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if p.empty:
            return None

        # حساب مؤشرات متعددة
        stability = max(0, min(100, 100 - (p.std() / p.mean() * 100) if p.mean() > 0 else 80))
        growth = max(0, min(100, (p.max() - p.min()) / p.min() * 10 if p.min() > 0 else 50))
        opportunity = max(0, min(100, (p.quantile(0.75) - p.quantile(0.25)) / p.median() * 100 if p.median() > 0 else 60))
        
        # المؤشر العام
        overall_index = (stability + growth + opportunity) / 3

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=overall_index,
            domain={'x': [0, 1], 'y': [0.5, 1]},
            title={'text': "المؤشر التنفيذي العام", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': self.COLORS["text"]},
                'bar': {'color': self.COLORS["primary"], 'thickness': 0.3},
                'steps': [
                    {'range': [0, 40], 'color': self.COLORS["light"]},
                    {'range': [40, 70], 'color': self.COLORS["pale"]},
                    {'range': [70, 100], 'color': self.COLORS["secondary"]}
                ],
                'threshold': {
                    'line': {'color': self.COLORS["accent"], 'width': 4},
                    'thickness': 0.75,
                    'value': overall_index
                }
            }
        ))

        # إضافة المؤشرات الفرعية
        sub_indicators = [
            ("الاستقرار", stability, self.COLORS["light"]),
            ("النمو", growth, self.COLORS["pale"]),
            ("الفرص", opportunity, self.COLORS["accent"]),
        ]

        for i, (label, value, color) in enumerate(sub_indicators):
            fig.add_trace(go.Indicator(
                mode="number",
                value=value,
                domain={'x': [i/3, (i+1)/3], 'y': [0, 0.4]},
                title={'text': label, 'font': {'size': 16}},
                number={'font': {'size': 28, 'color': color}, 'suffix': '%'}
            ))

        fig.update_layout(
            title="لوحة القيادة التنفيذية",
            grid={'rows': 2, 'columns': 3, 'pattern': "independent"},
            height=700
        )

        return self._safe(fig, height=700, is_executive=True)

    # =====================
    # CHAPTER 7 – الملخص التنفيذي
    # =====================
    def ch7_executive_summary(self, df):
        """ملخص تنفيذي شامل"""
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if p.empty:
            return None

        # إحصائيات أساسية
        stats = {
            "min": p.min(),
            "q1": p.quantile(0.25),
            "median": p.median(),
            "q3": p.quantile(0.75),
            "max": p.max(),
            "mean": p.mean(),
            "std": p.std(),
            "count": len(p)
        }

        fig = go.Figure()

        # دائرة تنفيذية كبيرة
        segments = {
            "اقتصادي": p[p < p.quantile(0.25)].count(),
            "متوسط": p[(p >= p.quantile(0.25)) & (p <= p.quantile(0.75))].count(),
            "فاخر": p[p > p.quantile(0.75)].count()
        }

        fig.add_trace(go.Pie(
            values=list(segments.values()),
            labels=list(segments.keys()),
            hole=0.7,
            marker=dict(
                colors=[self.COLORS["light"], self.COLORS["secondary"], self.COLORS["accent"]]
            ),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=16)
        ))

        # نص تنفيذي في المنتصف
        summary_text = (
            f"<b>تقرير تنفيذي</b><br><br>"
            f"📊 إجمالي العقارات: {stats['count']:,}<br>"
            f"💰 متوسط السوق: {stats['mean']:,.0f} ريال<br>"
            f"📈 نطاق السعر: {stats['min']:,.0f} - {stats['max']:,.0f}<br>"
            f"⚖️  معامل التباين: {(stats['std']/stats['mean']*100):.1f}%"
        )

        fig.add_annotation(
            text=summary_text,
            x=0.5,
            y=0.5,
            font=dict(size=18, color=self.COLORS["text"]),
            showarrow=False,
            align="center",
            bordercolor=self.COLORS["primary"],
            borderwidth=1,
            borderpad=10,
            bgcolor="rgba(255,255,255,0.9)"
        )

        fig.update_layout(
            title="الملخص التنفيذي الشامل",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            )
        )

        return self._safe(fig, height=650, is_executive=True)

    # =====================
    # CHAPTER 8 – الخاتمة
    # =====================
    def ch8_final_insight(self, df):
        """خاتمة بصرية هادئة"""
        if "price" not in df.columns:
            return None

        p = self._numeric(df["price"]).dropna()
        if len(p) < 10:
            return None

        # توزيع ناعم للخاتمة
        hist_y, hist_x = np.histogram(p, bins=20, density=True)
        hist_x = (hist_x[:-1] + hist_x[1:]) / 2

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hist_x,
                y=hist_y,
                mode="lines",
                line=dict(color=self.COLORS["primary"], width=3),
                fill="tozeroy",
                fillcolor="rgba(27,94,32,0.08)",
                name="التوزيع النهائي",
                smooth=True  # إضافة: تخطيط ناعم
            )
        )

        # إضافة خطوط إرشادية خفيفة
        for percentile, color in [(25, self.COLORS["light"]), (50, self.COLORS["accent"]), (75, self.COLORS["pale"])]:
            value = np.percentile(p, percentile)
            fig.add_vline(
                x=value,
                line=dict(color=color, width=1, dash="dot"),
                opacity=0.5
            )

        fig.update_layout(
            title="الخاتمة البصرية - نظرة نهائية",
            xaxis_title="السعر (ريال)",
            yaxis_title="الكثافة",
            showlegend=False
        )

        return self._safe(fig, height=500)

    # =====================
    # ENGINE
    # =====================
    def generate_all_charts(self, df):
        """محرك توليد الرسومات مع توزيع استراتيجي"""
        if df is None or df.empty:
            return {}

        def clean(lst):
            return [x for x in lst if x is not None]

        return {
            # الفصل 1: فهم السوق (تعديل: إعادة ترتيب الرسومات)
            "chapter_1": clean([
                self.ch1_scatter_flow(df),           # رسم كبير - العلاقة الأساسية
                self.ch1_market_overview(df),        # رسم متوسط - نظرة عامة
                self.ch1_price_distribution(df),     # رسم متوسط - التوزيع
            ]),
            
            # الفصل 2: الزمن (رسم كبير + رسم متوسط)
            "chapter_2": clean([
                self.ch2_price_stream(df),           # رسم كبير
                self.ch2_area_ribbon(df),            # رسم متوسط
            ]),
            
            # الفصل 3: البيانات (جدول + تحليل جودة)
            "chapter_3": clean([
                self.ch3_data_table(df),             # جدول
                self.ch3_data_quality(df),           # تحليل جودة (يبقى Bar Chart)
            ]),
            
            # الفصل 4: التحليل الاستراتيجي (رادار كبير)
            "chapter_4": clean([
                self.ch4_strategic_radar(df),        # رسم كبير
            ]),
            
            # الفصل 5: الفرص (رسم كبير + رسم متوسط)
            "chapter_5": clean([
                self.ch5_opportunity_bubble(df),     # رسم كبير
                self.ch5_value_distribution(df),     # رسم متوسط
            ]),
            
            # الفصل 6: القرار (مؤشر تنفيذي كبير)
            "chapter_6": clean([
                self.ch6_executive_gauge(df),        # رسم كبير جداً
            ]),
            
            # الفصل 7: الملخص التنفيذي (دائرة تنفيذية كبيرة)
            "chapter_7": clean([
                self.ch7_executive_summary(df),      # رسم كبير
            ]),
            
            # الفصل 8: الخاتمة (رسم هادئ)
            "chapter_8": clean([
                self.ch8_final_insight(df),          # رسم ختامي
            ]),
            
            # فصول احتياطية (فارغة حسب الخطة)
            "chapter_9": [],
            "chapter_10": [],
        }
