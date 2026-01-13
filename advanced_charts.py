import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class AdvancedCharts:

    # =========================
    # الفصل الأول
    # السيناريو الواقعي لمستقبل السوق
    # =========================

    def chapter_1_price_distribution(self, df):
        prices = df['السعر']
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(prices, bins=30, density=True, alpha=0.7)
        ax.set_title('توزيع أسعار العقارات في السوق')
        ax.set_xlabel('السعر')
        ax.set_ylabel('الكثافة')
        return fig

    def chapter_1_price_vs_area(self, df):
        area = df['المساحة']
        price = df['السعر']
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(area, price, alpha=0.6)
        if len(area) > 1:
            z = np.polyfit(area, price, 1)
            p = np.poly1d(z)
            ax.plot(area, p(area), linestyle='--')
        ax.set_title('العلاقة بين السعر والمساحة')
        ax.set_xlabel('المساحة (م²)')
        ax.set_ylabel('السعر')
        return fig

    def chapter_1_future_scenarios(self, df):
        avg_price = df['السعر'].mean()
        years = np.arange(0, 11)
        conservative = avg_price * (1 + 0.02) ** years
        realistic = avg_price * (1 + 0.05) ** years
        optimistic = avg_price * (1 + 0.08) ** years
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(years, conservative, label='سيناريو متحفظ')
        ax.plot(years, realistic, label='سيناريو واقعي')
        ax.plot(years, optimistic, label='سيناريو متفائل')
        ax.set_title('السيناريو الواقعي لمستقبل السوق خلال 10 سنوات')
        ax.set_xlabel('السنوات')
        ax.set_ylabel('السعر المتوقع')
        ax.legend()
        return fig

    # =========================
    # الفصل الثاني
    # المخاطر الخفية في السوق
    # =========================

    def chapter_2_price_concentration(self, df):
        prices = df['السعر']
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.boxplot(prices, vert=False)
        ax.set_title('مخاطر تركز الأسعار في السوق')
        ax.set_xlabel('السعر')
        return fig

    def chapter_2_price_volatility(self, df):
        price_bins = pd.qcut(df['السعر'], q=5, duplicates='drop')
        volatility = df.groupby(price_bins)['السعر'].std()
        fig, ax = plt.subplots(figsize=(8, 6))
        volatility.plot(kind='bar', ax=ax)
        ax.set_title('مؤشر التذبذب داخل شرائح الأسعار')
        ax.set_xlabel('شريحة السعر')
        ax.set_ylabel('الانحراف المعياري')
        return fig

    def chapter_2_overpricing_risk(self, df):
        price_per_sqm = df['السعر'] / df['المساحة']
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(price_per_sqm, bins=30, alpha=0.7)
        ax.axvline(price_per_sqm.mean(), linestyle='--', label='المتوسط')
        ax.set_title('مخاطر التسعير المبالغ فيه (السعر/م²)')
        ax.set_xlabel('السعر لكل متر مربع')
        ax.set_ylabel('عدد العقارات')
        ax.legend()
        return fig

        # =========================
    # الفصل الثالث
    # الفرص غير المرئية في السوق
    # =========================

    def chapter_3_value_map(self, df):
        """
        Page 1:
        Value Map
        خريطة القيمة (السعر لكل متر مقابل المساحة)
        """
        price_per_sqm = df['السعر'] / df['المساحة']

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df['المساحة'], price_per_sqm, alpha=0.6)
        ax.axhline(price_per_sqm.mean(), linestyle='--', label='متوسط السعر/م²')
        ax.set_title('خريطة القيمة في السوق')
        ax.set_xlabel('المساحة (م²)')
        ax.set_ylabel('السعر لكل متر مربع')
        ax.legend()

        return fig


    def chapter_3_affordable_pockets(self, df):
        """
        Page 2:
        Affordable Pockets
        جيوب الفرص منخفضة السعر
        """
        price_per_sqm = df['السعر'] / df['المساحة']
        threshold = price_per_sqm.quantile(0.3)
        filtered = df[price_per_sqm <= threshold]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(filtered['السعر'], bins=20, alpha=0.7)
        ax.set_title('العقارات ذات القيمة العالية مقابل السعر')
        ax.set_xlabel('السعر')
        ax.set_ylabel('عدد العقارات')

        return fig


    def chapter_3_size_opportunities(self, df):
        """
        Page 3:
        Size-Based Opportunities
        فرص الاستثمار حسب فئات المساحة
        """
        bins = [0, 80, 120, 180, 300, df['المساحة'].max()]
        labels = ['صغيرة', 'متوسطة', 'متوسطة-كبيرة', 'كبيرة', 'كبيرة جدًا']

        df['فئة_المساحة'] = pd.cut(
            df['المساحة'],
            bins=bins,
            labels=labels,
            include_lowest=True
        )

        avg_price = df.groupby('فئة_المساحة')['السعر'].mean()

        fig, ax = plt.subplots(figsize=(8, 6))
        avg_price.plot(kind='bar', ax=ax)
        ax.set_title('متوسط السعر حسب فئة المساحة')
        ax.set_xlabel('فئة المساحة')
        ax.set_ylabel('متوسط السعر')

        return fig

        # =========================
    # الفصل الرابع
    # خطة التعامل الذكي مع السوق
    # =========================

    def chapter_4_investment_allocation_logic(self, df):
        """
        Page 1:
        Smart Allocation Logic
        منطق توزيع الاستثمار
        """
        price_per_sqm = df['السعر'] / df['المساحة']

        # تصنيف العقارات حسب القيمة
        conditions = [
            price_per_sqm <= price_per_sqm.quantile(0.3),
            (price_per_sqm > price_per_sqm.quantile(0.3)) & (price_per_sqm <= price_per_sqm.quantile(0.7)),
            price_per_sqm > price_per_sqm.quantile(0.7)
        ]
        labels = ['فرصة قوية', 'منطقة مراقبة', 'مخاطرة مرتفعة']

        df['تصنيف_الاستثمار'] = np.select(conditions, labels)

        allocation = df['تصنيف_الاستثمار'].value_counts()

        fig, ax = plt.subplots(figsize=(8, 6))
        allocation.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('توزيع العقارات حسب منطق الاستثمار')
        ax.set_ylabel('')

        return fig


    def chapter_4_action_matrix(self, df):
        """
        Page 2:
        Action Matrix
        مصفوفة القرار (اشترِ / انتظر / تجنّب)
        """
        price_per_sqm = df['السعر'] / df['المساحة']
        df['إجراء'] = np.where(
            price_per_sqm <= price_per_sqm.quantile(0.3), 'اشترِ',
            np.where(
                price_per_sqm <= price_per_sqm.quantile(0.7), 'انتظر',
                'تجنّب'
            )
        )

        action_counts = df['إجراء'].value_counts()

        fig, ax = plt.subplots(figsize=(8, 6))
        action_counts.plot(kind='bar', ax=ax)
        ax.set_title('مصفوفة القرار الاستثماري')
        ax.set_xlabel('الإجراء')
        ax.set_ylabel('عدد العقارات')

        return fig

        # =========================
    # الفصل الخامس
    # التوقيت في السوق
    # =========================

    def chapter_5_price_positioning(self, df):
        """
        Page 1:
        Market Positioning
        موقع الأسعار داخل نطاق السوق
        """
        prices = df['السعر']
        q1 = prices.quantile(0.25)
        q2 = prices.quantile(0.50)
        q3 = prices.quantile(0.75)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(prices, bins=30, alpha=0.7)

        ax.axvline(q1, linestyle='--', label='الربع الأدنى')
        ax.axvline(q2, linestyle='--', label='الوسيط')
        ax.axvline(q3, linestyle='--', label='الربع الأعلى')

        ax.set_title('موقع الأسعار داخل نطاق السوق')
        ax.set_xlabel('السعر')
        ax.set_ylabel('عدد العقارات')
        ax.legend()

        return fig


    def chapter_5_entry_timing_signal(self, df):
        """
        Page 2:
        Entry Timing Signal
        إشارة توقيت الدخول
        """
        prices = df['السعر']

        signals = pd.cut(
            prices,
            bins=[
                prices.min(),
                prices.quantile(0.3),
                prices.quantile(0.7),
                prices.max()
            ],
            labels=['دخول قوي', 'مراقبة', 'تريث']
        )

        signal_counts = signals.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 6))
        signal_counts.plot(kind='bar', ax=ax)
        ax.set_title('إشارات توقيت الدخول إلى السوق')
        ax.set_xlabel('إشارة التوقيت')
        ax.set_ylabel('عدد العقارات')

        return fig

        # =========================
    # الفصل السادس
    # توزيع رأس المال
    # =========================

    def chapter_6_capital_allocation_by_risk(self, df):
        """
        Page 1:
        Capital Allocation by Risk
        توزيع رأس المال حسب مستوى المخاطرة
        """
        price_per_sqm = df['السعر'] / df['المساحة']

        risk_levels = pd.cut(
            price_per_sqm,
            bins=[
                price_per_sqm.min(),
                price_per_sqm.quantile(0.3),
                price_per_sqm.quantile(0.7),
                price_per_sqm.max()
            ],
            labels=['مخاطرة منخفضة', 'مخاطرة متوسطة', 'مخاطرة مرتفعة']
        )

        risk_distribution = risk_levels.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 6))
        risk_distribution.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('توزيع الفرص حسب مستوى المخاطرة')
        ax.set_ylabel('')

        return fig


    def chapter_6_capital_balance_curve(self, df):
        """
        Page 2:
        Capital Balance Curve
        منحنى توازن العائد والمخاطرة
        """
        price_per_sqm = df['السعر'] / df['المساحة']

        risk_score = (price_per_sqm - price_per_sqm.min()) / (
            price_per_sqm.max() - price_per_sqm.min()
        )

        expected_return = 1 - risk_score

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(risk_score, expected_return, alpha=0.6)
        ax.set_title('منحنى توازن العائد مقابل المخاطرة')
        ax.set_xlabel('مستوى المخاطرة')
        ax.set_ylabel('العائد المتوقع')

        return fig

        # =========================
    # الفصل السابع
    # متى تخرج؟ ومتى تبقى؟
    # =========================

    def chapter_7_exit_pressure_zones(self, df):
        """
        Page 1:
        Exit Pressure Zones
        مناطق ضغط الخروج
        """
        price_per_sqm = df['السعر'] / df['المساحة']

        zones = pd.cut(
            price_per_sqm,
            bins=[
                price_per_sqm.min(),
                price_per_sqm.quantile(0.4),
                price_per_sqm.quantile(0.75),
                price_per_sqm.max()
            ],
            labels=['منطقة أمان', 'منطقة مراقبة', 'منطقة ضغط خروج']
        )

        zone_counts = zones.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 6))
        zone_counts.plot(kind='bar', ax=ax)
        ax.set_title('مناطق ضغط الخروج في السوق')
        ax.set_xlabel('منطقة القرار')
        ax.set_ylabel('عدد العقارات')

        return fig


    def chapter_7_hold_vs_exit_signal(self, df):
        """
        Page 2:
        Hold vs Exit Signal
        إشارة البقاء مقابل الخروج
        """
        price_per_sqm = df['السعر'] / df['المساحة']
        median_value = price_per_sqm.median()

        signal = np.where(
            price_per_sqm <= median_value,
            'احتفظ',
            'فكّر بالخروج'
        )

        signal_counts = pd.Series(signal).value_counts()

        fig, ax = plt.subplots(figsize=(8, 6))
        signal_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('إشارة البقاء مقابل الخروج')
        ax.set_ylabel('')

        return fig

        # =========================
    # الفصل الثامن
    # الإشارات المبكرة في السوق
    # =========================

    def chapter_8_anomaly_detection(self, df):
        """
        Page 1:
        Early Anomaly Signals
        الإشارات غير الطبيعية المبكرة
        """
        price_per_sqm = df['السعر'] / df['المساحة']

        mean = price_per_sqm.mean()
        std = price_per_sqm.std()

        anomalies = df[(price_per_sqm < mean - 2 * std) | (price_per_sqm > mean + 2 * std)]
        normal = df.drop(anomalies.index)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(normal['المساحة'], normal['السعر'] / normal['المساحة'], alpha=0.4, label='طبيعي')
        ax.scatter(anomalies['المساحة'], anomalies['السعر'] / anomalies['المساحة'],
                   color='red', label='إشارات مبكرة')
        ax.set_title('الإشارات غير الطبيعية المبكرة في السوق')
        ax.set_xlabel('المساحة (م²)')
        ax.set_ylabel('السعر لكل متر مربع')
        ax.legend()

        return fig


    def chapter_8_signal_intensity(self, df):
        """
        Page 2:
        Signal Intensity Index
        مؤشر قوة الإشارات المبكرة
        """
        price_per_sqm = df['السعر'] / df['المساحة']
        z_scores = (price_per_sqm - price_per_sqm.mean()) / price_per_sqm.std()

        intensity = pd.cut(
            z_scores,
            bins=[-np.inf, -1.5, 1.5, np.inf],
            labels=['إشارة ضعيفة', 'وضع طبيعي', 'إشارة قوية']
        )

        intensity_counts = intensity.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 6))
        intensity_counts.plot(kind='bar', ax=ax)
        ax.set_title('مؤشر قوة الإشارات المبكرة')
        ax.set_xlabel('قوة الإشارة')
        ax.set_ylabel('عدد العقارات')

        return fig
