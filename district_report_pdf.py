# =========================================
# Warda Intelligence
# District Report PDF Builder
# =========================================

from fpdf import FPDF
import os
import plotly.io as pio
from advanced_charts import AdvancedCharts


class DistrictReportPDF:

    def __init__(self):
        self.pdf = FPDF()
        self.charts_engine = AdvancedCharts()

    # =====================
    # HEADER
    # =====================

    def add_cover(self, district, city):

        self.pdf.add_page()

        self.pdf.set_font("Arial", "B", 22)
        self.pdf.cell(0, 20, "Warda Intelligence", ln=True)

        self.pdf.set_font("Arial", "", 16)
        self.pdf.cell(0, 10, f"District Investment Report", ln=True)

        self.pdf.ln(10)

        self.pdf.set_font("Arial", "", 14)
        self.pdf.cell(0, 10, f"City: {city}", ln=True)
        self.pdf.cell(0, 10, f"District: {district}", ln=True)

        self.pdf.ln(20)

    # =====================
    # TEXT SECTIONS
    # =====================

    def add_text_section(self, title, text):

        self.pdf.add_page()

        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, title, ln=True)

        self.pdf.ln(5)

        self.pdf.set_font("Arial", "", 12)

        for line in text.split("\n"):
            self.pdf.multi_cell(0, 8, line)

    # =====================
    # CHART PAGE
    # =====================

    def add_chart(self, fig, title):

        if fig is None:
            return

        self.pdf.add_page()

        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, title, ln=True)

        img_path = "temp_chart.png"

        pio.write_image(fig, img_path, width=1000, height=600)

        self.pdf.image(img_path, x=10, y=30, w=190)

        os.remove(img_path)

    # =====================
    # BUILD REPORT
    # =====================

    def build_report(
        self,
        df,
        district,
        city,
        narrative_text,
        nearby_districts
    ):

        # غلاف
        self.add_cover(district, city)

        # النص التحليلي
        self.add_text_section(
            "District Investment Analysis",
            narrative_text
        )

        # الرسومات
        charts = self.charts_engine.generate_all_district_charts(
            df,
            district,
            nearby_districts
        )

        for name, fig in charts.items():

            title_map = {
                "price_trend": "Price Trend",
                "district_comparison": "District Comparison",
                "transactions_over_time": "Transactions Over Time",
                "price_distribution": "Price Distribution",
                "property_type_analysis": "Property Type Analysis"
            }

            title = title_map.get(name, name)

            self.add_chart(fig, title)

        return self.pdf
