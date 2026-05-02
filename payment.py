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
def create_payment(amount, report_name):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8501/?payment=success",
            "cancel_url": "http://localhost:8501/?payment=cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": report_name,
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
        payment_id = payment.id
        for link in payment.links:
            if link.rel == "approval_url":
                return str(link.href), payment_id
    return None, None

# ✅ تأكيد عملية الدفع
def execute_payment(payment_id, payer_id):
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        return True
    return False
