"""
Report Orchestrator
-------------------
Gatekeeper نهائي للتقرير

- يبني المحتوى النصي من report_content_builder
- يربط الرسومات حسب الفصول
- يطبق سياسة الرسومات حسب الباقات
- يُخرج:
    - content_text
    - charts_by_chapter
"""

# ===================== IMPORTS =====================
from datetime import datetime
import re
import pandas as pd
import numpy as np

from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts

# ===================== VISUAL POLICY =====================
# عدد الرسومات الداعمة المسموح بها لكل باقة
PACKAGE_VISUAL_POLICY = {
    "مجانية": 0,
    "فضية": 1,
    "ذهبية": 2,
    "ماسية": 3,
    "ماسية متميزة": 5,
}

# ===================== INIT =====================
charts_engine = AdvancedCharts()

# ===================== DATA NORMALIZATION =====================
def normalize_dataframe(data):
    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        return data if not data.empty else None

    if isinstance(data, dict):
        try:
            df = pd.DataFrame(data)
            return df if not df.empty else None
        except Exception:
            return None

    return None


def ensure_required_columns(df):
    """
    نضمن وجود الأعمدة التي تحتاجها الرسومات
    (حتى لا ينكسر أي رسم بسبب نقص بيانات)
    """
    if df is None or df.empty:
        return None

    required_defaults = {
        "price": np.random.randint(500_000, 3_000_000, len(df)),
        "area": np.random.randint(80, 300, len(df)),
        "date": pd.date_range("2023-01-01", periods=len(df), freq="M"),
        "rental_yield": np.random.uniform(3.0, 8.0, len(df)),
        "location_score": np.random.randint(1, 10, len(df)),
        "time_on_market": np.random.randint(10, 120, len(df)),
        "demand_index": np.random.uniform(0.5, 1.5, len(df)),
        "signal_strength": np.random.uniform(0, 1, len(df)),
        "entry_signal": np.random.randint(0, 2, len(df)),
        "growth_rate": np.random.uniform(-2, 5, len(df)),
    }

    for col, generator in required_defaults.items():
        if col not in df.columns:
            df[col] = generator

    return df


# ===================== USER INFO PREP =====================
def prepare_user_info_for_content(user_info):
    """
    تحويل user_info إلى الصيغة التي يتوقعها report_content_builder
    """
    if user_info is None:
        user_info = {}

    package = (
        user_info.get("package")
        or user_info.get("chosen_pkg")
        or user_info.get("باقة")
        or "مجانية"
    )

    prepared = {
        "المدينة": user_info.get("city", "المدينة"),
        "نوع_العقار": user_info.get("property_type", "العقار"),
        "نوع_الصفقة": user_info.get("status", "الاستثمار"),
        "package": package,
    }

    return prepared


# ===================== BLOCKS → TEXT =====================
def blocks_to_text(report):
    """
    يحوّل بلوكات المحتوى إلى نص متسلسل نظيف
    مع تنظيف الخطوط الزخرفية
    """
    lines = []

    for chapter in report.get("chapters", []):
        for block in chapter.get("blocks", []):
            block_type = block.get("type")
            content = block.get("content")

            if not content:
                continue

            # عنوان فصل
            if block_type == "chapter_title":
                lines.append(content.strip())
                lines.append("")
                continue

            # تجاهل أي بلوك رسم (نحن نربط الرسومات لاحقًا)
            if block_type == "chart":
                continue

            if isinstance(content, str):
                for raw_line in content.splitlines():
                    clean = raw_line.strip()

                    if not clean:
                        lines.append("")
                        continue

                    # إزالة الخطوط الزخرفية
                    if re.fullmatch(r"[-–—_=\s]*", clean):
                        continue

                    lines.append(clean)

                lines.append("")

    return "\n".join(lines)


# ===================== CHARTS BY PACKAGE =====================
def generate_charts_by_package(df, package):
    """
    يولّد الرسومات حسب الفصول
    ثم يطبّق سياسة الباقة:
    - Hero دائمًا
    - Supporting حسب الباقة
    """
    raw_charts = charts_engine.generate_all(df)
    allowed_supporting = PACKAGE_VISUAL_POLICY.get(package, 0)

    final = {}

    for chapter_key, charts in raw_charts.items():
        if not charts or "hero" not in charts:
            continue

        final[chapter_key] = []

        # 🥇 Hero Chart (دائمًا)
        final[chapter_key].append(charts["hero"])

        # 🥈 Supporting Charts (حسب الباقة)
        supporting = charts.get("supporting", [])
        if supporting and allowed_supporting > 0:
            final[chapter_key].extend(supporting[:allowed_supporting])

    return final


# ===================== CORE ORCHESTRATOR =====================
def build_report_story(user_info, dataframe=None):
    """
    يبني تقريرًا جاهزًا للـ PDF:
    - content_text
    - charts_by_chapter
    """

    # -----------------------------
    # PACKAGE
    # -----------------------------
    package = (
        user_info.get("package")
        or user_info.get("chosen_pkg")
        or user_info.get("باقة")
        or "مجانية"
    )

    # -----------------------------
    # CONTENT
    # -----------------------------
    prepared_user_info = prepare_user_info_for_content(user_info)
    report = build_complete_report(prepared_user_info)

    if report and "chapters" in report:
        content_text = blocks_to_text(report)
    else:
        content_text = f"""
الفصل الأول – مقدمة
هذا تقرير تجريبي.

المدينة: {user_info.get('city', 'غير محدد')}
نوع العقار: {user_info.get('property_type', 'غير محدد')}
الباقة: {package}
"""

    # -----------------------------
    # DATA
    # -----------------------------
    df = normalize_dataframe(dataframe)
    df = ensure_required_columns(df)

    # -----------------------------
    # CHARTS
    # -----------------------------
    charts_by_chapter = {}
    if df is not None:
        charts_by_chapter = generate_charts_by_package(df, package)

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    return {
        "meta": {
            "package": str(package),
            "generated_at": datetime.now().isoformat(),
        },
        "content_text": content_text,
        "charts": charts_by_chapter,
    }
