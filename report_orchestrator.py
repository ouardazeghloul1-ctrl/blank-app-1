# report_orchestrator.py
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
import pandas as pd
import numpy as np
from datetime import datetime


charts_engine = AdvancedCharts()


def normalize_dataframe(df):
    if df is None or df.empty:
        return None
    return df


def ensure_required_columns(df):
    defaults = {
        "price": np.random.randint(500_000, 3_000_000, len(df)),
        "area": np.random.randint(80, 300, len(df)),
        "date": pd.date_range("2023-01-01", periods=len(df), freq="M"),
    }
    for col, gen in defaults.items():
        if col not in df.columns:
            df[col] = gen
    return df


def blocks_to_text(report):
    lines = []
    for chapter in report["chapters"]:
        for block in chapter["blocks"]:
            content = block.get("content", "")
            if content:
                lines.append(content.strip())
                lines.append("")
    return "\n".join(lines)


def build_report_story(user_info, dataframe=None):
    """
    ⚠️ هذه الدالة تُستدعى مباشرة من streamlit_app.py
    لا تغيّري توقيعها
    """

    prepared = {
        "المدينة": user_info.get("city", ""),
        "نوع_العقار": user_info.get("property_type", ""),
        "نوع_الصفقة": user_info.get("status", ""),
        "package": user_info.get("package") or user_info.get("chosen_pkg") or "مجانية",
    }

    report = build_complete_report(prepared)
    content_text = blocks_to_text(report)

    df = normalize_dataframe(dataframe)
    if df is not None:
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
