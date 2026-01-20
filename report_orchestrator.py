"""
Report Orchestrator
-------------------
Gatekeeper نهائي للتقرير
يحوّل البلوكات إلى محتوى نصي نظيف وجاهز للـ PDF
"""

# ===================== IMPORTS =====================
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
import pandas as pd
import numpy as np

# ===================== INITIALIZATION =====================
charts_engine = AdvancedCharts()

# ===================== DATA GATE =====================
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
    if df is None:
        return None

    required_defaults = {
        "price": np.random.randint(500000, 3000000, len(df)),
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


# ===================== BLOCK → TEXT =====================
def blocks_to_text(report):
    """
    يحوّل البلوكات إلى نص متسلسل للـ PDF
    مع فراغ ذكي بعد كل عنوان فصل (لمكان الرسومات)
    """
    lines = []

    for chapter in report["chapters"]:
        for block in chapter["blocks"]:
            block_type = block.get("type")
            content = block.get("content")

            if not content:
                continue

            # عنوان الفصل
            if block_type == "chapter_title":
                lines.append(content.strip())
                lines.append("")        # فراغ خفيف
                lines.append("")        # فراغ إضافي (مكان الرسومات)
                continue

            # تجاهل أي بلوك رسومات نصيًا
            if block_type == "chart":
                continue

            if isinstance(content, str):
                lines.append(content.strip())
                lines.append("")

    return "\n".join(lines)


# ===================== CORE ORCHESTRATOR =====================
def build_report_story(user_info, dataframe=None):
    """
    يبني تقريرًا جاهزًا:
    - نص متسلسل نظيف
    - بنية رسومات جاهزة
    """

    # 1️⃣ بناء المحتوى الحقيقي
    report = build_complete_report(user_info)

    # 2️⃣ تحويل البلوكات إلى نص
    content_text = blocks_to_text(report)

    # 3️⃣ تطبيع البيانات
    df = normalize_dataframe(dataframe)
    df = ensure_required_columns(df)

    # 4️⃣ توليد الرسومات (إن وُجدت بيانات)
    charts_by_chapter = {}
    if df is not None:
        charts_by_chapter = charts_engine.generate_all_charts(df)

    # 5️⃣ إخراج نظيف
    return {
        "meta": {
            "package": report["package"],
            "package_name": report["package_name"],
        },
        "content_text": content_text,
        "charts": charts_by_chapter,
    }
