import matplotlib.pyplot as plt
import numpy as np

class AdvancedCharts:

    # =========================
    # الفصل الأول
    # السيناريو الواقعي لمستقبل السوق
    # =========================

    def chapter_1_price_distribution(self, df):
        """
        Page 1:
        Market Price Landscape
        توزيع أسعار العقارات
        """
        prices = df['السعر']

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(prices, bins=30, density=True, alpha=0.7)
        ax.set_title('توزيع أسعار العقارات في السوق')
        ax.set_xlabel('السعر')
        ax.set_ylabel('الكثافة')

        return fig


    def chapter_1_price_vs_area(self, df):
        """
        Page 2:
        Market Health
        السعر مقابل المساحة
        """
        area = df['المساحة']
        price = df['السعر']

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(area, price, alpha=0.6)
        
        # خط الاتجاه
        if len(area) > 1:
            z = np.polyfit(area, price, 1)
            p = np.poly1d(z)
            ax.plot(area, p(area), linestyle='--')

        ax.set_title('العلاقة بين السعر والمساحة')
        ax.set_xlabel('المساحة (م²)')
        ax.set_ylabel('السعر')

        return fig


    def chapter_1_future_scenarios(self, df):
        """
        Page 3:
        10-Year Realistic Scenarios
        السيناريوهات المستقبلية لعشر سنوات
        """
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
