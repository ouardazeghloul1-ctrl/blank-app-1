import streamlit as st
import pandas as pd
import io
from advanced_charts import AdvancedCharts
from report_pdf_generator import create_pdf_from_content
from district_narrative_engine import generate_district_narrative
from government_data_provider import load_projects_data, load_districts_data  # ✅ إضافة جديدة


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

    # =========================================
    # تحويل البيانات إلى أرقام فقط - بدون حذف أي صفقة
    # =========================================
    city_data["price"] = pd.to_numeric(city_data["price"], errors="coerce")
    city_data["area"] = pd.to_numeric(city_data["area"], errors="coerce")
    
    # لا يتم حذف أي صفقة - الاحتفاظ بجميع الصفقات كما هي
    
    # -------- المرحلة 4: استخراج الأحياء النشطة فقط (5 صفقات فأكثر) --------
    district_col = "district_clean" if "district_clean" in city_data.columns else "district"
    
    # ✅ تنظيف اسم الحي قبل حساب عدد الصفقات
    district_counts = (
        city_data[district_col]
        .astype(str)
        .str.split("/")
        .str[-1]
        .str.strip()
        .value_counts()
        .sort_values(ascending=False)
    )
    
    # الأحياء النشطة = أكثر من 5 صفقات
    active_districts = district_counts[district_counts >= 5]
    
    # تنظيف اسم الحي من اسم المدينة (مثل "جدة / المروة" لتصبح "المروة")
    districts = [
        str(d).split("/")[-1].strip() 
        for d in active_districts.index.tolist() 
        if d not in ["غير محدد", "", None]
    ]

    if not districts:
        st.error(f"❌ لا توجد أحياء نشطة (بـ 5 صفقات أو أكثر) في مدينة {city}")
        districts = []  # قائمة فارغة لتجنب الأخطاء

    # -------- المرحلة 5: اختيار الحي (فقط إذا وجدت أحياء) --------
    if districts:
        district = st.selectbox("اختر الحي", districts, key="district_select")

        # -------- المرحلة 6: اختيار نوع العقار --------
        property_type = st.selectbox(
            "نوع العقار", 
            ["شقة", "تاون هاوس", "فيلا", "أرض", "محل تجاري"],
            key="property_type_select"
        )

        # -------- المرحلة 7: فلترة البيانات حسب الحي فقط (بدون فلترة نوع العقار) --------
        # فلترة الحي فقط - مع تنظيف الاسم من المدينة
        district_data = city_data[
            city_data[district_col]
            .astype(str)
            .str.split("/")
            .str[-1]
            .str.strip()
            .str.lower() == district.lower()
        ].copy()
        
        # =========================================
        # ✅ التعديل الأول: حساب عدد صفقات الحي الكلي وعدد صفقات نوع العقار
        # =========================================
        district_transactions_total = len(district_data)
        
        # التأكد من وجود عمود property_type في البيانات
        if "property_type" in district_data.columns:
            property_transactions_count = len(
                district_data[
                    district_data["property_type"]
                    .astype(str)
                    .str.strip()
                    .str.lower() == property_type.lower()
                ]
            )
        else:
            # إذا لم يوجد العمود، نستخدم العدد الكلي كقيمة احتياطية
            property_transactions_count = district_transactions_total
        
        # ✅ إضافة عمود بنوع العقار المحدد للاستخدام في الرسومات
        district_data["selected_property_type"] = property_type
        
        # ✅ تم إزالة فلترة نوع العقار بالكامل - نعتمد على user_info فقط

        # ✅ للاختبار: عرض عدد الصفقات بعد الفلترة
        st.write("عدد الصفقات بعد الفلترة:", len(district_data))

        # التحقق من وجود بيانات
        if district_data.empty:
            st.warning(f"⚠️ لا توجد صفقات في حي {district}")
        else:
            # عرض إحصائيات سريعة
            st.success(f"📊 تحليل {property_type} في حي {district} - {city}")
            
            col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
            
            with col_metrics1:
                st.metric("عدد الصفقات", len(district_data))
            
            with col_metrics2:
                # ✅ استخدام median مع dropna لمنع NaN
                avg_price = district_data["price"].dropna().median()
                st.metric("متوسط السعر", f"{avg_price:,.0f} ريال" if pd.notna(avg_price) else "غير متوفر")
            
            with col_metrics3:
                # حساب سعر المتر فقط للصفقات الصالحة - بدون حذف الصفقات
                valid_area = district_data[
                    (district_data["price"].notna()) & 
                    (district_data["area"].notna()) & 
                    (district_data["area"] > 0)
                ]
                if not valid_area.empty:
                    # ✅ استخدام median بدلاً من mean
                    district_price_per_m2 = (valid_area["price"] / valid_area["area"]).median()
                    st.metric("متوسط سعر المتر", f"{district_price_per_m2:,.0f} ريال")
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
                        # توحيد أسماء الأعمدة مع حماية من التضارب
                        if "district_clean" in district_data.columns and "district" not in district_data.columns:
                            district_data = district_data.rename(columns={"district_clean": "district"})
                        
                        # حساب متوسط سعر المتر للحي - فقط من الصفقات الصالحة
                        valid_area_data = district_data[
                            (district_data["price"].notna()) & 
                            (district_data["area"].notna()) & 
                            (district_data["area"] > 0)
                        ]
                        
                        if not valid_area_data.empty:
                            # ✅ استخدام median بدلاً من mean
                            district_price_per_m2 = (valid_area_data["price"] / valid_area_data["area"]).median()
                        else:
                            district_price_per_m2 = 0
                        
                        # حساب متوسط سعر المتر للمدينة - فقط من الصفقات الصالحة
                        valid_city_area = city_data[
                            (city_data["price"].notna()) & 
                            (city_data["area"].notna()) & 
                            (city_data["area"] > 0)
                        ]
                        if not valid_city_area.empty:
                            # ✅ استخدام median بدلاً من mean
                            city_price_per_m2 = (valid_city_area["price"] / valid_city_area["area"]).median()
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
                            "transactions_count": len(district_data),  # عدد الصفقات كامل (حتى الناقصة)
                            "price_deviation_percent": round(price_deviation_percent, 1)
                        }
                        
                        # حساب DPI حسب قوة الحي
                        if len(district_data) >= 50:
                            dpi_score = 85
                        elif len(district_data) >= 30:
                            dpi_score = 75
                        elif len(district_data) >= 20:
                            dpi_score = 65
                        elif len(district_data) >= 10:
                            dpi_score = 55
                        elif len(district_data) >= 5:
                            dpi_score = 45
                        else:
                            dpi_score = 35
                            
                        # تحسين إضافي: إضافة عامل السعر
                        if district_price_per_m2 > city_price_per_m2 * 1.2:
                            dpi_score = min(95, dpi_score + 10)
                        elif district_price_per_m2 < city_price_per_m2 * 0.8:
                            dpi_score = max(30, dpi_score - 5)
                        
                        # =========================================
                        # ✅ التعديل الأساسي: جلب إحداثيات الحي وبيانات المشاريع
                        # =========================================
                        projects_df = load_projects_data()
                        districts_df = load_districts_data()
                        
                        district_lat = None
                        district_lon = None
                        district_impact = None
                        
                        if districts_df is not None and not districts_df.empty:
                            district_row = districts_df[
                                districts_df["اسم الحي"]
                                .astype(str)
                                .str.strip()
                                .str.contains(str(district).strip(), case=False, na=False)
                            ].head(1)
                            if not district_row.empty:
                                district_lat = district_row.iloc[0].get("خط_العرض", None)
                                district_lon = district_row.iloc[0].get("خط_الطول", None)
                                district_impact = district_row.iloc[0].get("نطاق_التأثير", 5)
                                
                                # 🔴🔴🔴 التعديل الحاسم - إجبار نطاق التأثير على 10 كم كحد أدنى 🔴🔴🔴
                                try:
                                    district_impact = max(float(district_impact), 10)
                                except (ValueError, TypeError):
                                    district_impact = 10  # قيمة افتراضية 10 كم
                        
                        # =========================================
                        # ✅ التعديل الثاني: تعديل user_info بإضافة المفتاحين الجديدين واستبدال transactions_count
                        # =========================================
                        user_info = {
                            # المفاتيح المطلوبة من report_pdf_generator.py
                            "city_name": city,
                            "district_name": district,
                            "property_type": property_type,
                            "district_avg_price": district_price_per_m2,
                            "city_avg_price": city_price_per_m2,
                            # ✅ تم استبدال transactions_count بالمفتاحين التاليين
                            "district_transactions_total": district_transactions_total,
                            "property_transactions_count": property_transactions_count,
                            "dpi_score": dpi_score,
                            "total_transactions": len(district_data),  # ✅ إضافة إجمالي الصفقات (للتطابق مع بعض الوظائف)
                            
                            # مفاتيح إضافية للاستخدام الداخلي
                            "package": "ذهبية",
                            "user_type": "مستثمر",
                            "analysis_mode": "district",
                            
                            # ✅ المفاتيح الجديدة للخريطة والمشاريع
                            "خط_العرض": district_lat,
                            "خط_الطول": district_lon,  # ✅ تم التصحيح: خط_الطول (مع الـ "ال")
                            "نطاق_التأثير": district_impact,
                            "projects_data": projects_df
                        }
                        
                        # =========================================
                        # تجهيز بيانات الأحياء المجاورة
                        # استخدام الأحياء النشطة فقط وأول 10 أحياء فقط
                        # =========================================
                        nearby_districts = []
                        for d in districts[:10]:  # استخدام أول 10 أحياء فقط
                            if d != district and pd.notna(d) and d not in ["غير محدد", ""]:
                                # تنظيف اسم الحي أثناء الفلترة
                                d_data = city_data[
                                    city_data[district_col]
                                    .astype(str)
                                    .str.split("/")
                                    .str[-1]
                                    .str.strip()
                                    .str.lower() == d.lower()
                                ]
                                if not d_data.empty and "area" in d_data.columns:
                                    # حساب متوسط سعر المتر للأحياء المجاورة - فقط من الصفقات الصالحة
                                    d_valid_area = d_data[
                                        (d_data["price"].notna()) & 
                                        (d_data["area"].notna()) & 
                                        (d_data["area"] > 0)
                                    ]
                                    if not d_valid_area.empty:
                                        avg_price = (d_valid_area["price"] / d_valid_area["area"]).median()
                                        nearby_districts.append({
                                            "district_name": d,
                                            "avg_price": avg_price
                                        })
                        
                        # =========================================
                        # استخدام محرك الأحياء لتوليد النص
                        # ✅ السطر المطلوب: projects_data=projects_df تم إضافته أدناه
                        # =========================================
                        report_text = generate_district_narrative(
                            user_info=user_info,
                            district_metrics=district_metrics,
                            nearby_districts=nearby_districts,
                            dpi_score=dpi_score,
                            market_data=city_data,
                            real_data=city_data,
                            projects_data=projects_df  # ✅ هذا هو السطر المطلوب
                        )
                        
                        # استخدام city_data للرسومات
                        charts_engine = AdvancedCharts()
                        raw_charts = charts_engine.generate_all_district_charts(
                            city_data,
                            district
                        )
                        
                        # =========================================
                        # ✅ التعديل المهم: تغيير أرقام الفصول لتتوافق مع محرك PDF
                        # الفصول التي تحتوي على رسومات: 4, 7, 11, 16, 21
                        # =========================================
                        charts_by_chapter = {
                            "chapter_4": [raw_charts.get("price_trend")],
                            "chapter_7": [raw_charts.get("district_comparison")],
                            "chapter_11": [raw_charts.get("transactions_over_time")],
                            "chapter_16": [raw_charts.get("price_distribution")],
                            "chapter_21": [raw_charts.get("property_type_analysis")],
                        }
                        
                        # تنظيف الرسومات الفارغة
                        for k in charts_by_chapter:
                            charts_by_chapter[k] = [c for c in charts_by_chapter[k] if c is not None]
                        
                        # -------- المرحلة 10: إنشاء ملف PDF --------
                        pdf_buffer = create_pdf_from_content(
                            user_info=user_info,
                            content_text=report_text,
                            executive_decision="",
                            charts_by_chapter=charts_by_chapter,
                            package_level="ذهبية"
                        )
                        
                        st.session_state.district_pdf_data = pdf_buffer.getvalue()
                        st.session_state.district_report_generated = True
                        
                        # عرض معلومات debug
                        print(f"🚀 DEBUG: تم إنشاء تقرير الحي بنجاح")
                        print(f"📊 DEBUG: DPI Score: {dpi_score}")
                        print(f"📊 DEBUG: عدد الأحياء المجاورة: {len(nearby_districts)}")
                        print(f"📊 DEBUG: نوع العقار المحدد: {property_type}")
                        print(f"📊 DEBUG: عدد صفقات الحي الكلي: {district_transactions_total}")
                        print(f"📊 DEBUG: عدد صفقات نوع العقار: {property_transactions_count}")
                        print(f"📍 DEBUG: إحداثيات الحي - خط العرض: {district_lat}, خط الطول: {district_lon}")
                        print(f"🎯 DEBUG: نطاق التأثير: {district_impact} (النوع: {type(district_impact).__name__})")
                        print(f"🔑 DEBUG: مفاتيح user_info: {list(user_info.keys())}")
                        
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
