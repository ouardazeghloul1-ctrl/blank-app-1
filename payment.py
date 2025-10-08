import paypalrestsdk
import os
from dotenv import load_dotenv

load_dotenv()

# 🔐 إعدادات PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # استخدمي "live" بعد اختبار الموقع
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_SECRET")
})

# ✅ إنشاء عملية الدفع
def create_payment(amount):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8501",
            "cancel_url": "http://localhost:8501"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "تقرير العقارات الذكي",
                    "sku": "RealAI",
                    "price": str(amount),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {"total": str(amount), "currency": "USD"},
            "description": "شراء تقرير تحليل العقارات باستخدام الذكاء الاصطناعي"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return str(link.href)
    return None

# ✅ تأكيد عملية الدفع
def execute_payment(payment_id, payer_id):
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        return True
    return False
