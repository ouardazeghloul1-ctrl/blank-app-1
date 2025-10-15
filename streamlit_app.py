# === الواجهة الرئيسية ===
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 بيانات المستخدم")
    
    user_type = st.selectbox("اختر فئتك:", 
                           ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
    
    city = st.selectbox("المدينة:", 
                       ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"])
    
    property_type = st.selectbox("نوع العقار:", 
                                ["شقة", "فيلا", "أرض", "محل تجاري"])
    
    status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
    
    area = st.slider("المساحة (م²):", 50, 1000, 120)

with col2:
    st.markdown("### 💎 اختيار الباقة")
    
    # عدد العقارات مع تحديث السعر تلقائياً
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 1, 50, 1,
                              help="كلما زاد عدد العقارات، زادت دقة التحليل والسعر")
    
    # عرض الباقات
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
    
    # حساب السعر الديناميكي
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price * property_count
    
    # عرض تفاصيل الباقة
    st.markdown(f"""
    <div class='package-card'>
    <h3>باقة {chosen_pkg}</h3>
    <h4>{total_price} دولار</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض المميزات
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"✅ {feature}")

# === نظام الدفع ===
st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")

# زر الدفع باي بال
paypal_html = f"""
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="warda.intelligence@gmail.com">
<input type="hidden" name="item_name" value="تقرير {chosen_pkg} - {property_count} عقار">
<input type="hidden" name="amount" value="{total_price}">
<input type="hidden" name="currency_code" value="USD">
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!" style="display: block; margin: 0 auto;">
</form>
"""

st.markdown(paypal_html, unsafe_allow_html=True)

# === زر واحد لإنشاء التقرير ===
st.markdown("---")
st.markdown("### 🚀 إنشاء التقرير")

col1, col2 = st.columns(2)

with col1:
    # زر للمسؤول (بدون دفع)
    if st.button("🎯 إنشاء التقرير (للمسؤول)", use_container_width=True):
        with st.spinner("🔄 جاري إنشاء التقرير المتقدم..."):
            time.sleep(3)
            
            # إنشاء التقرير المتقدم
            report, final_price = generate_advanced_report(
                user_type, city, property_type, area, status, chosen_pkg, property_count
            )
            
            # حفظ التقرير في الجلسة
            st.session_state.current_report = report
            st.session_state.report_generated = True
            st.success("✅ تم إنشاء التقرير المتقدم!")

with col2:
    # زر للعميل (بعد الدفع)
    if st.button("📥 تحميل التقرير (بعد الدفع)", use_container_width=True):
        if hasattr(st.session_state, 'current_report'):
            st.success("✅ تم تحميل التقرير")
        else:
            st.warning("⚠️ يرجى إتمام عملية الدفع أولاً")

# === عرض التقرير وزر التحميل ===
if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي المتقدم")
    
    # عرض التقرير
    st.text_area("محتوى التقرير:", st.session_state.current_report, height=600)
    
    # زر تحميل التقرير
    st.download_button(
        label="📥 تحميل التقرير الكامل (PDF)",
        data=st.session_state.current_report,
        file_name=f"تقرير_متقدم_{user_type}_{city}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.success("🎉 تم إنشاء التقرير المتقدم بنجاح! يحتوي على 5 صفحات من التحليل الشامل")
    st.balloons()

# === لوحة المسؤول ===
admin_password = st.sidebar.text_input("كلمة مرور المسؤول:", type="password")
if admin_password == "WardaAdmin2024":
    st.sidebar.success("🎉 مرحباً بك في لوحة التحكم!")
    
    # لوحة تحكم المسؤول
    st.sidebar.markdown("### 🛠️ لوحة تحكم المسؤول")
    
    if st.sidebar.button("🔗 إنشاء رابط مؤثرين جديد"):
        today = datetime.now().strftime("%Y%m%d")
        influencer_token = hashlib.md5(f"FREE1_{today}_{np.random.randint(1000,9999)}".encode()).hexdigest()[:10]
        st.session_state.influencer_url = f"https://warda-intelligence.streamlit.app/?promo={influencer_token}"
        st.sidebar.success("✅ تم إنشاء الرابط الجديد")
    
    if hasattr(st.session_state, 'influencer_url'):
        st.sidebar.markdown(f"**رابط المؤثرين:**")
        st.sidebar.code(st.session_state.influencer_url)

# === باقي الكود يبقى كما هو ===
