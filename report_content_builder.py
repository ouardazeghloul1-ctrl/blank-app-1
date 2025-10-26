import matplotlib.pyplot as plt
import pandas as pd

def create_analysis_charts(market_data, real_data, user_info):
    import matplotlib.pyplot as plt
    import pandas as pd

    charts = []

    # ✅ تنظيف بيانات السعر قبل التحليل
    if real_data is not None and not real_data.empty:
        real_data = real_data.copy()
        real_data["السعر"] = pd.to_numeric(real_data["السعر"], errors="coerce")
        real_data.dropna(subset=["السعر"], inplace=True)

    # ✅ إذا لا توجد بيانات نرجع رسم فارغ بدل كسر الكود
    if real_data is None or real_data.empty:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.text(0.5, 0.5, "لا توجد بيانات كافية للعرض", ha='center', va='center', fontsize=14)
        ax.axis('off')
        return [fig]

    # ---------------------------------------------------------
    # 🎨 الرسم 1 — توزيع الأسعار
    # ---------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(10,6))
    ax1.hist(real_data["السعر"], bins=20)
    ax1.set_title("توزيع الأسعار في السوق")
    ax1.set_xlabel("السعر")
    ax1.set_ylabel("عدد العقارات")
    charts.append(fig1)

    # ---------------------------------------------------------
    # 🎨 الرسم 2 — متوسط الأسعار حسب المنطقة (إن وجدت)
    # ---------------------------------------------------------
    if "المنطقة" in real_data.columns:
        mean_by_area = real_data.groupby("المنطقة")["السعر"].mean().sort_values()
        fig2, ax2 = plt.subplots(figsize=(10,6))
        mean_by_area.plot(kind='bar', ax=ax2)
        ax2.set_title("متوسط السعر حسب المنطقة")
        ax2.set_xlabel("المنطقة")
        ax2.set_ylabel("متوسط السعر")
        charts.append(fig2)

    # ---------------------------------------------------------
    # 🎨 الرسم 3 — توجهات الأسعار عبر الزمن (إذا توفرت بيانات السوق)
    # ---------------------------------------------------------
    if market_data is not None and not market_data.empty and "price_index" in market_data.columns:
        fig3, ax3 = plt.subplots(figsize=(10,6))
        ax3.plot(market_data["date"], market_data["price_index"])
        ax3.set_title("توجهات الأسعار عبر الزمن")
        ax3.set_xlabel("الزمن")
        ax3.set_ylabel("مؤشر السعر")
        charts.append(fig3)

    return charts
