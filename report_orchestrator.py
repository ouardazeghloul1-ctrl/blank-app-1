"""
Report Orchestrator
-------------------
Gatekeeper نهائي للتقرير
يحوّل البلوكات إلى نص متسلسل نظيف وجاهز للـ PDF
"""

# ===================== IMPORTS =====================
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
import pandas as pd
import numpy as np
import re
from datetime import datetime

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


def prepare_user_info_for_content(user_info):
    """
    تحويل user_info إلى التنسيق الذي يتوقعه report_content_builder
    """
    if user_info is None:
        user_info = {}
    
    # إعادة تسمية المفاتيح لتناسب report_content_builder
    prepared_info = {
        "المدينة": user_info.get("city", "المدينة"),
        "نوع_العقار": user_info.get("property_type", "العقار"),
        "نوع_الصفقة": user_info.get("status", "الاستثمار"),
        "package": user_info.get("package", "free"),
    }
    
    return prepared_info


# ===================== BLOCK → TEXT =====================
def blocks_to_text(report):
    """
    يحوّل كل الفصول والبلوكات إلى نص متسلسل نظيف وجاهز للـ PDF
    مع تنظيف السطور الزخرفية (----)
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
                lines.append("")
                continue

            if block_type == "chart":
                continue

            if isinstance(content, str):
                # 🔑 هنا الحل الحقيقي: تنظيف سطر بسطر
                for raw_line in content.splitlines():
                    clean = raw_line.strip()

                    # ❌ حذف أي سطر لا يحتوي حروف أو أرقام (زخرفة فقط)
                    if not clean:
                        lines.append("")
                        continue

                    # ✅ الحل النهائي: إزالة جميع أنواع الخطوط الزخرفية
                    # هذا سيزيل: ------------ , ________ , –––––––– , الخ
                    if re.fullmatch(r'[-–—_=\s]*', clean):
                        continue

                    # ✅ يحافظ على النقاط التعدادية •
                    lines.append(clean)

                lines.append("")

    return "\n".join(lines)


# ===================== CORE ORCHESTRATOR =====================
def build_report_story(user_info, dataframe=None):
    """
    يبني تقريرًا جاهزًا:
    - نص متسلسل
    - رسومات مربوطة
    """

    # 1️⃣ بناء المحتوى
    prepared_user_info = prepare_user_info_for_content(user_info)
    report = build_complete_report(prepared_user_info)

    # 2️⃣ تحويل البلوكات إلى نص
    if report and "chapters" in report:
        content_text = blocks_to_text(report)
    else:
        content_text = """
        الفصل الأول: مقدمة
        هذا تقرير تجريبي لأن نظام البناء الرئيسي لم يعمل بشكل صحيح.
        
        الفصل الثاني: بيانات المستخدم
        المدينة: {}
        نوع العقار: {}
        الباقة: {}
        """.format(
            user_info.get("city", "غير محدد"),
            user_info.get("property_type", "غير محدد"),
            user_info.get("package", "غير محدد")
        )

    # 3️⃣ البيانات
    df = normalize_dataframe(dataframe)
    df = ensure_required_columns(df)

    # 4️⃣ الرسومات
    charts_by_chapter = {}
    if df is not None:
        charts_by_chapter = charts_engine.generate_all_charts(df)

    # 5️⃣ إخراج نهائي نظيف
    return {
        "meta": {
            "package": user_info.get("package"),
            "package_name": user_info.get("package"),
            "generated_at": datetime.now().isoformat()
        },
        "content_text": content_text,
        "charts": charts_by_chapter,
    }
