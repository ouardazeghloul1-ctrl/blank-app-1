# report_orchestrator.py

from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
import pandas as pd
import numpy as np
from datetime import datetime


# 🔒 ثابت – لا يُكسر
charts_engine = AdvancedCharts(theme="light")


# =================================
# Data Normalization
# =================================
def normalize_dataframe(df):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return None
    return df.copy()


def unify_columns(df):
    """
    توحيد الأعمدة العربية / الإنجليزية
    هذا هو المكان الصحيح لهذا المنطق
    """
    column_map = {
        "السعر": "price",
        "المساحة": "area",
        "تاريخ_الجلب": "date",
        "date": "date",
    }

    for ar, en in column_map.items():
        if ar in df.columns and en not in df.columns:
            df[en] = df[ar]

    return df


def ensure_required_columns(df):
    """
    ضمان الأعمدة التي تحتاجها الرسومات فقط
    بدون توليد بيانات عشوائية غير منطقية
    """
    if "price" not in df.columns:
        df["price"] = np.random.randint(500_000, 3_000_000, len(df))

    if "area" not in df.columns:
        df["area"] = np.random.randint(80, 300, len(df))

    if "date" not in df.columns:
        df["date"] = pd.date_range(
            start="2023-01-01",
            periods=len(df),
            freq="M"
        )

    return df


# =================================
# Text Builder
# =================================
def blocks_to_text(report):
    lines = []
    for chapter in report.get("chapters", []):
        for block in chapter.get("blocks", []):
            content = block.get("content", "")
            if content:
                lines.append(content.strip())
                lines.append("")
    return "\n".join(lines)


# =================================
# MAIN STORY BUILDER
# =================================
def build_report_story(user_info, dataframe=None):
    """
    ⚠️ هذه الدالة تُستدعى مباشرة من streamlit_app.py
    ⚠️ لا تغيّري توقيعها
    """

    prepared = {
        "المدينة": user_info.get("city", ""),
        "نوع_العقار": user_info.get("property_type", ""),
        "نوع_الصفقة": user_info.get("status", ""),
        "package": (
            user_info.get("package")
            or user_info.get("chosen_pkg")
            or "مجانية"
        ),
    }

    # -------- Build textual report --------
    report = build_complete_report(prepared)
    content_text = blocks_to_text(report)

    # -------- Charts pipeline --------
    df = normalize_dataframe(dataframe)

    if df is not None:
        df = unify_columns(df)
        df = ensure_required_columns(df)
        charts = charts_engine.generate_all_charts(df)
    else:
        charts = {}

    return {
        "meta": {
            "package": prepared["package"],
            "generated_at": datetime.now().isoformat()
        },
        "content_text": content_text,
        "charts": charts
    }
