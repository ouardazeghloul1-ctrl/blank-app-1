import streamlit as st
import os
from realfetcher import get_real_data
from ai_predictor import analyze_results
from payment import create_payment, execute_payment
from dotenv import load_dotenv

# تحميل بيانات باي بال
load_dotenv()

st.set_page_config(page_title="البحث الاحترافي", page_icon="🔍", layout="centered")

# 🎨 عنوان الصفحة
st.title("🔍 أداة البحث الاحترافي بالذكاء الاصطناعي")
st.write("ابحث بذكاء، حلّل بدقة، وادفع بثقة 💫")

# 🟦 اختيار نوع البحث
search_type = st.radio("اختر نوع البحث:", ["🔹 البحث السريع (19$)", "⚡ البحث الدقيق (49$)", "👑 البحث المتقدم المخصص (999$)"])

# 🟢 خانة البحث
query = st.text_input("أدخل الكلمة أو الجملة التي تريد البحث عنها:")

# 🧭 زر البحث
if st.button("ابدأ البحث"):
    if not query:
        st.warning("🟠 من فضلك أدخل كلمة البحث أولاً.")
    else:
        st.info("🔎 جاري البحث، يرجى الانتظار قليلاً...")

        # 🔍 جلب البيانات
        results = get_real_data(query)
        if not results:
            st.error("❌ لم يتم العثور على نتائج، حاول بكلمة أخرى.")
        else:
            # 🤖 تحليل النتائج بالذكاء الاصطناعي
            analyzed = analyze_results(results)

            # عرض جزء مجاني قبل الدفع
            st.subheader("📊 جزء من النتائج المجانية:")
            st.dataframe(analyzed.head(5))

            st.markdown("---")
            st.info("💡 لمشاهدة التقرير الكامل يجب إتمام الدفع أدناه 👇")

            # 🪙 الدفع حسب الخطة
            if search_type == "🔹 البحث السريع (19$)":
                amount = 19
            elif search_type == "⚡ البحث الدقيق (49$)":
                amount = 49
            else:
                amount = 999

            # 🔗 إنشاء رابط الدفع
            payment_url = create_payment(amount)

            if payment_url:
                st.markdown(f"[💳 اضغط هنا لإتمام الدفع عبر PayPal]({payment_url})")
            else:
                st.error("⚠️ حدث خطأ أثناء إنشاء الدفع، يرجى المحاولة لاحقاً.")

# ✅ عند رجوع المستخدم بعد الدفع
payment_id = st.query_params.get("paymentId")
payer_id = st.query_params.get("PayerID")

if payment_id and payer_id:
    if execute_payment(payment_id, payer_id):
        st.success("✅ تم الدفع بنجاح! إليك التقرير الكامل 👇")

        # عرض النتائج الكاملة
        results = get_real_data(query)
        analyzed = analyze_results(results)
        st.dataframe(analyzed)

        # تحميل التقرير كـ PDF
        csv = analyzed.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 تحميل التقرير كملف CSV",
            data=csv,
            file_name=f"report_{query}.csv",
            mime="text/csv"
        )
    else:
        st.error("❌ فشل في تأكيد الدفع، يرجى المحاولة مرة أخرى.")
