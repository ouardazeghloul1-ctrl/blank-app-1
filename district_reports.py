import streamlit as st
import pandas as pd
import io
from advanced_charts import AdvancedCharts
from report_pdf_generator import create_pdf_from_content
from district_narrative_engine import generate_district_narrative


def show_district_reports(df_raw):
    """
    عرض تقارير الأحياء بشكل منفصل عن الملف الرئيسي
    """
    st.markdown("## 📍 تحليل الأحياء")

    # -------- المرحلة 1: تحديد المدن الخمس فقط --------
    cities = ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام"]

    # -------- المرحلة 2: اختيار المدينة --------
    city = st.selectbox("اختر المدينة", cities, key="district_city_select")

    # -------- المرحلة 3: استخراج بيانات المدينة - استخدام contains للتعامل مع صيغ متعددة --------
    city_data = df_raw[
        df_raw["city"]
        .astype(str)
        .str.strip()
        .str.contains(city, case=False, na=False)
    ].copy()

    # -------- المرحلة 4: استخراج الأحياء النشطة فقط (5 صفقات فأكثر) --------
    district_col = "district_clean" if "district_clean" in city_data.columns else "district"
    
    # حساب عدد الصفقات لكل حي
    district_counts = (
        city_data[district_col]
        .value_counts()
        .sort_values(ascending=False)
    )
    
    # الأحياء النشطة = أكثر من 5 صفقات
    active_districts = district_counts[district_counts >= 5]
    districts = active_districts.index.tolist()
    
    # إزالة الأحياء غير الصالحة
    districts = [d for d in districts if d not in ["غير محدد", "", None]]

    if not districts:
        st.error(f"❌ لا توجد أحياء نشطة (بـ 5 صفقات أو أكثر) في مدينة {city}")
        districts = []  # قائمة فارغة لتجنب الأخطاء

    # -------- المرحلة 5: اختيار الحي (فقط إذا وجدت أحياء) --------
    if districts:
        district = st.selectbox("اختر الحي", districts, key="district_select")

        # -------- المرحلة 6: اختيار نوع العقار --------
        property_type = st.selectbox(
            "نوع العقار", 
            ["شقة", "فيلا", "أرض", "محل تجاري"],
            key="property_type_select"
        )

        # -------- المرحلة 7: فلترة البيانات حسب الحي ونوع العقار --------
        # تحويل نوع العقار إلى التصنيف الداخلي
        property_map = {
            "شقة": "سكني",
            "فيلا": "سكني",
            "محل تجاري": "تجاري",
            "أرض": "أرض"
        }
        property_category = property_map.get(property_type, "سكني")
            
        district_data = city_data[
            (city_data[district_col].astype(str).str.strip() == district) & 
            (city_data["property_type"] == property_category)
        ].copy()

        # التحقق من وجود بيانات
        if district_data.empty:
            st.warning(f"⚠️ لا توجد صفقات لنوع العقار {property_type} في حي {district}")
        else:
            # عرض إحصائيات سريعة
            st.success(f"📊 تحليل {property_type} في حي {district} - {city}")
            
            col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
            
            with col_metrics1:
                st.metric("عدد الصفقات", len(district_data))
            
            with col_metrics2:
                district_data["price"] = pd.to_numeric(district_data["price"], errors="coerce")
                avg_price = district_data["price"].mean()
                st.metric("متوسط السعر", f"{avg_price:,.0f} ريال" if pd.notna(avg_price) else "غير متوفر")
            
            with col_metrics3:
                district_data["area"] = pd.to_numeric(district_data["area"], errors="coerce")
                valid_area = district_data[district_data["area"] > 0]
                if not valid_area.empty:
                    avg_price_per_sqm = (valid_area["price"] / valid_area["area"]).mean()
                    st.metric("متوسط سعر المتر", f"{avg_price_per_sqm:,.0f} ريال")
                else:
                    st.metric("متوسط سعر المتر", "غير متوفر")

            # -------- المرحلة 8: زر إنشاء تقرير الحي --------
            generate_report_clicked = st.button(
                "📄 إنشاء تقرير الحي",
                use_container_width=True,
                key="generate_district_report"
            )

            # -------- المرحلة 9: تشغيل محرك التقرير --------
            if generate_report_clicked:
                with st.spinner("🔄 جاري إنشاء تقرير الحي..."):
                    try:
                        # توحيد أسماء الأعمدة للرسومات البيانية
                        if "district_clean" in district_data.columns:
                            district_data = district_data.rename(columns={"district_clean": "district"})
                        
                        # التأكد من أن البيانات رقمية للرسومات
                        district_data["price"] = pd.to_numeric(district_data["price"], errors="coerce")
                        district_data["area"] = pd.to_numeric(district_data["area"], errors="coerce")
                        
                        # تنظيف البيانات قبل توليد الرسومات
                        district_data = district_data.dropna(subset=["price", "area"])
                        district_data = district_data[district_data["area"] > 0]
                        
                        # حساب مؤشرات الحي مع التأكد من عدم وجود قيم صفرية في المساحة
                        valid_area_data = district_data[district_data["area"] > 0]
                        
                        if not valid_area_data.empty:
                            district_price_per_m2 = (valid_area_data["price"] / valid_area_data["area"]).mean()
                        else:
                            district_price_per_m2 = 0
                        
                        valid_city_area = city_data[city_data["area"] > 0]
                        if not valid_city_area.empty:
                            city_price_per_m2 = (valid_city_area["price"] / valid_city_area["area"]).mean()
                        else:
                            city_price_per_m2 = 0
                        
                        # حساب نسبة الانحراف
                        price_deviation_percent = ((district_price_per_m2 - city_price_per_m2) / city_price_per_m2 * 100) if city_price_per_m2 > 0 else 0
                        
                        # مؤشرات الحي بالصيغة الصحيحة
                        district_metrics = {
                            "district_name": district,
                            "city_name": city,
                            "district_avg_price": district_price_per_m2,
                            "city_avg_price": city_price_per_m2,
                            "transactions_count": len(district_data),
                            "price_deviation_percent": round(price_deviation_percent, 1)
                        }
                        
                        # إعداد معلومات المستخدم للتقرير
                        user_info = {
                            "city": city,
                            "district": district,
                            "property_type": property_type,
                            "package": "ذهبية",  # استخدام الباقة الذهبية للتقارير المتقدمة
                            "user_type": "مستثمر",
                            "analysis_mode": "district"
                        }
                        
                        # استخدام محرك الأحياء لتوليد النص
                        report_text = generate_district_narrative(
                            user_info=user_info,
                            district_metrics=district_metrics,
                            nearby_districts=[],
                            dpi_score=50,
                            market_data={},
                            real_data=district_data
                        )
                        
                        # توليد الرسومات البيانية للحي
                        charts_engine = AdvancedCharts()
                        raw_charts = charts_engine.generate_all_district_charts(
                            district_data,
                            district
                        )
                        
                        # توحيد شكل الرسومات ليطابق محرك PDF مع دعم جميع الفصول
                        charts_by_chapter = {
                            "chapter_1": [raw_charts.get("price_trend")],
                            "chapter_2": [raw_charts.get("district_comparison")],
                            "chapter_3": [raw_charts.get("transactions_over_time")],
                            "chapter_4": [raw_charts.get("price_distribution")],
                            "chapter_5": [raw_charts.get("property_type_analysis")],
                            "chapter_6": [],
                            "chapter_7": [],
                            "chapter_8": [],
                        }
                        
                        # تنظيف الرسومات الفارغة (إزالة القيم None)
                        for k in charts_by_chapter:
                            charts_by_chapter[k] = [c for c in charts_by_chapter[k] if c is not None]
                        
                        # -------- المرحلة 10: إنشاء ملف PDF باستخدام نفس نظام المدن --------
                        pdf_buffer = create_pdf_from_content(
                            user_info=user_info,
                            content_text=report_text,
                            executive_decision="",  # فارغ مؤقتاً لتجنب ظهور أقسام فارغة
                            charts_by_chapter=charts_by_chapter,
                            package_level="ذهبية"
                        )
                        
                        st.session_state.district_pdf_data = pdf_buffer.getvalue()
                        st.session_state.district_report_generated = True
                        
                        # عرض معلومات debug للمطور (تظهر فقط في terminal)
                        print(f"🚀 DEBUG: تم إنشاء تقرير الحي بنجاح باستخدام نظام PDF الموحد")
                        print(f"📊 DEBUG: عدد فصول الرسومات: {len(charts_by_chapter)}")
                        for chapter, figs in charts_by_chapter.items():
                            # التحقق من نوع figs قبل استخدام len()
                            if not isinstance(figs, list):
                                figs = [figs]
                            print(f"   - {chapter}: {len(figs)} رسم بياني")
                        
                        st.success("✅ تم إنشاء تقرير الحي بنجاح!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ خطأ في إنشاء تقرير الحي: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())

    # -------- المرحلة 11: زر تحميل التقرير --------
    if st.session_state.get('district_report_generated', False) and st.session_state.get('district_pdf_data') is not None:
        district_name = district if 'district' in locals() and district else "district"
        file_name = f"warda_district_report_{city}_{district_name}_{property_type}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        st.download_button(
            label="📥 تحميل تقرير الحي PDF",
            data=st.session_state.district_pdf_data,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True,
            key="download_district_report"
        )
