"""
Report Orchestrator
-------------------
محرك تنسيق وبناء التقرير النهائي
يربط بين:
- report_content_builder
- advanced_charts
- واجهة العرض (Streamlit / PDF)

إصدار: 1.1.0 (Chart-Key Safe)
"""

# ===================== IMPORTS =====================
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts

# ===================== INITIALIZATION =====================
charts_engine = AdvancedCharts()


# ===================== CORE ORCHESTRATOR =====================
def build_report_story(user_info, dataframe=None):
    """
    يبني التقرير النهائي الجاهز للعرض
    بدون أي منطق محتوى داخلي
    """

    # 1️⃣ بناء التقرير المفلتر حسب الباقة
    report = build_complete_report(user_info)

    # 2️⃣ توليد الرسومات (إن وُجدت بيانات)
    charts_by_chapter = {}
    if dataframe is not None:
        charts_by_chapter = charts_engine.generate_all_charts(dataframe)

    # 3️⃣ فهرسة كل الرسومات بواسطة chart_key (الحل الجذري)
    chart_index = {}

    for chapter_key, figs in charts_by_chapter.items():
        for fig in figs:
            if fig is None:
                continue
            meta = getattr(fig, "meta", {})
            chart_key = meta.get("chart_key")
            if chart_key:
                chart_index[chart_key] = fig

    # 4️⃣ ربط الرسومات بالبلوكات باستخدام chart_key فقط
    for chapter in report["chapters"]:
        for block in chapter["blocks"]:
            if block.get("type") == "chart":
                block_chart_key = block.get("chart_key")
                block["figure"] = chart_index.get(block_chart_key)

    # 5️⃣ إخراج التقرير النهائي
    return {
        "meta": {
            "package": report["package"],
            "package_name": report["package_name"],
            "stats": report["stats"]
        },
        "chapters": report["chapters"]
    }


# ===================== STREAMLIT RENDER =====================
def render_report_streamlit(report_data, st):
    """
    عرض التقرير داخل Streamlit
    """

    st.title("📊 التقرير الاستثماري العقاري المتقدم")

    # معلومات عامة
    meta = report_data["meta"]
    st.markdown(f"""
**الباقة:** {meta['package_name']}  
**عدد الفصول:** {meta['stats']['total_chapters']}  
**عدد الصفحات المتوقعة:** {meta['stats']['estimated_pages']}  
**عدد الرسومات:** {meta['stats']['total_charts']}  
""")

    # عرض الفصول
    for chapter in report_data["chapters"]:
        st.markdown("---")
        st.header(chapter["chapter_title"])

        for block in chapter["blocks"]:
            block_type = block.get("type")

            # تجاهل عنوان الفصل (عُرض بالفعل)
            if block_type == "chapter_title":
                continue

            # محتوى نصي
            elif block_type in [
                "chapter_context",
                "main_content",
                "advanced_analysis",
                "scenarios",
                "international_analysis",
                "chapter_conclusion",
                "final_conclusion",
                "how_to_read",
                "key_indicators"
            ]:
                st.markdown(block.get("content", ""))

            # الرسومات
            elif block_type == "chart":
                fig = block.get("figure")
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📉 الرسم غير متاح لعدم كفاية البيانات أو الأعمدة المطلوبة.")

    return True


# ===================== QUICK TEST =====================
if __name__ == "__main__":
    # اختبار سريع بدون Streamlit
    test_user = {
        "package": "ذهبية",  # عربي أو إنجليزي – كلاهما مدعوم
        "نوع_العقار": "شقق سكنية",
        "المدينة": "الرياض"
    }

    report = build_report_story(test_user, dataframe=None)

    print("✅ التقرير بُني بنجاح")
    print("الباقة:", report["meta"]["package_name"])
    print("الفصول:", len(report["chapters"]))
    print("الرسومات:", report["meta"]["stats"]["total_charts"])
