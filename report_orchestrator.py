"""
Report Orchestrator
-------------------
محرك تنسيق وبناء التقرير النهائي
يربط بين:
- report_content_builder
- advanced_charts
- واجهة العرض (Streamlit / PDF)

إصدار: 1.0.1 (Package normalization fix)
"""

# ===================== IMPORTS =====================
from report_content_builder import (
    build_complete_report,
    PACKAGE_ALIASES
)
from advanced_charts import AdvancedCharts

# ===================== INITIALIZATION =====================
charts_engine = AdvancedCharts()


# ===================== CORE ORCHESTRATOR =====================
def build_report_story(user_info, dataframe=None):
    """
    يبني التقرير النهائي الجاهز للعرض
    بدون أي منطق محتوى داخلي
    """

    # --------------------------------------------------
    # 🔒 توحيد اسم الباقة (عربي / إنجليزي → تقني)
    # --------------------------------------------------
    raw_package = user_info.get("package", "free")
    normalized_package = PACKAGE_ALIASES.get(raw_package)

    if not normalized_package:
        raise ValueError(
            f"نوع الباقة غير مدعوم: {raw_package}. "
            f"الباقات المدعومة: {', '.join(PACKAGE_ALIASES.keys())}"
        )

    # فرض الاسم التقني داخل النظام
    user_info["package"] = normalized_package

    # --------------------------------------------------
    # 1️⃣ بناء التقرير المفلتر حسب الباقة
    # --------------------------------------------------
    report = build_complete_report(user_info)

    # --------------------------------------------------
    # 2️⃣ توليد الرسومات (إن وُجدت بيانات)
    # --------------------------------------------------
    charts_by_chapter = {}
    if dataframe is not None:
        charts_by_chapter = charts_engine.generate_all_charts(dataframe)

    # --------------------------------------------------
    # 3️⃣ ربط الرسومات بالبلوكات
    # --------------------------------------------------
    for chapter in report["chapters"]:
        chapter_key = f"chapter_{chapter['chapter_number']}"

        for block in chapter["blocks"]:
            if block.get("type") == "chart":
                chart_key = block.get("chart_key")

                chart_obj = None
                if chapter_key in charts_by_chapter:
                    for fig in charts_by_chapter[chapter_key]:
                        if fig.layout.title.text == block.get("title"):
                            chart_obj = fig
                            break

                block["figure"] = chart_obj

    # --------------------------------------------------
    # 4️⃣ إخراج التقرير النهائي
    # --------------------------------------------------
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
""")

    # عرض الفصول
    for chapter in report_data["chapters"]:
        st.markdown("---")
        st.header(chapter["chapter_title"])

        for block in chapter["blocks"]:
            block_type = block.get("type")

            # العناوين
            if block_type == "chapter_title":
                continue

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

            elif block_type == "chart":
                fig = block.get("figure")
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📉 الرسم غير متاح لعدم كفاية البيانات.")

    return True


# ===================== QUICK TEST =====================
if __name__ == "__main__":
    # اختبار سريع بدون Streamlit
    test_user = {
        "package": "ماسية",  # ← عربي أو إنجليزي كلاهما يعمل الآن
        "نوع_العقار": "شقق سكنية",
        "المدينة": "الرياض"
    }

    report = build_report_story(test_user, dataframe=None)

    print("✅ التقرير بُني بنجاح")
    print("الباقة التقنية:", report["meta"]["package"])
    print("اسم الباقة:", report["meta"]["package_name"])
    print("الفصول:", len(report["chapters"]))
    print("الرسومات:", report["meta"]["stats"]["total_charts"])
