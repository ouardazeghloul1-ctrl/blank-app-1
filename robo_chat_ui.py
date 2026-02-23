import streamlit as st
from robo_advisor import handle_robo_question, RoboKnowledge, RoboGuard

# ==============================
# إعداد الصفحة
# ==============================
st.set_page_config(
    page_title="Robo Advisor – Warda Intelligence",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 المستشار الذكي – Warda Intelligence")

# ==============================
# Session State لحفظ المحادثة
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==============================
# بيانات المستخدم (مؤقتًا)
# ==============================
city = st.selectbox("اختر مدينتك", ["الرياض", "جدة", "الدمام"])
package = st.selectbox(
    "باقتك",
    ["مجانية", "فضية", "ذهبية", "ماسية", "ماسية متميزة"]
)

user_profile = {
    "city": city,
    "package": package
}

# ==============================
# بيانات تجريبية (سنربطها لاحقًا بالبيانات الحقيقية)
# ==============================
market_data = {
    "مؤشر_السيولة": 80,
    "معدل_النمو_الشهري": 2.5,
    "عدد_العقارات_الحقيقية": 1200
}

opportunities = {
    "عقارات_مخفضة": [
        {"المدينة": "الرياض", "المنطقة": "النرجس", "الخصم": "14%"},
        {"المدينة": "جدة", "المنطقة": "أبحر", "الخصم": "11%"}
    ]
}

knowledge = RoboKnowledge(None, opportunities, None, market_data)
guard = RoboGuard(package)

# ==============================
# عرض المحادثة السابقة
# ==============================
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# إدخال المستخدم
# ==============================
user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    # عرض سؤال المستخدم
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # توليد رد الروبو
    response = handle_robo_question(
        user_profile,
        knowledge,
        guard,
        user_input
    )

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)
