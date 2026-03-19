from district_report_factory import generate_all_district_reports
from government_data_provider import load_government_data

print("🚀 تشغيل المصنع...")

df = load_government_data()

# تقليل البيانات لتفادي التعليق
df = df.head(100)

generate_all_district_reports(df)

print("✅ انتهى")
