# advanced_charts.py
class AdvancedCharts:
    def create_all_charts(self, real_data, user_info):
        charts = []
        
        # رسم بياني بسيط
        if not real_data.empty:
            fig, ax = plt.subplots()
            real_data['المنطقة'].value_counts().head(5).plot(kind='bar', ax=ax)
            ax.set_title('توزيع العقارات حسب المنطقة')
            charts.append(fig)
        
        return charts
