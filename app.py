# app.py
import os
import uuid
import base64
import io
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, render_template_string, send_file
import matplotlib.pyplot as plt
import pandas as pd
import paypalrestsdk
from realfetcher import fetch_properties
from ai_predictor import train_price_predictor, predict_future_prices
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# load env
load_dotenv()
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")  # sandbox or live

# إعداد بايبال
if PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET:
    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET
    })
else:
    # ستكون المدفوعات معطلة إذا لم توفري المفاتيح
    print("⚠️ لم يتم العثور على مفاتيح PayPal في .env. وظائف الدفع معطلة حتى تضعي CLIENT_ID و SECRET.")

app = Flask(__name__)

# تخزين مؤقت للنتائج قبل/بعد الدفع (للتجربة على سيرفر محلي صغير)
ANALYSES = {}  # token -> dict {df_records, summary, pdf_bytes (بعد الدفع)}

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>وردة العقارية - تحليل ذكي</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style> body { background:#f8fafc; } .card { direction:rtl; } </style>
</head>
<body>
<div class="container py-4">
  <h2 class="text-center mb-4">🏡 وردة العقارية — تحليل عقاري ذكي</h2>
  <div class="card p-4">
    <form method="post" action="/analyze">
      <div class="row mb-3">
        <div class="col-md-4">
          <label class="form-label">المدينة</label>
          <select class="form-select" name="city">
            <option>الرياض</option>
            <option>جدة</option>
            <option>الدمام</option>
          </select>
        </div>
        <div class="col-md-4">
          <label class="form-label">نوع التحليل</label>
          <select class="form-select" name="mode">
            <option value="quick">⚡ سريع</option>
            <option value="deep">🔍 دقيق</option>
            <option value="vip">👑 مميز (VIP)</option>
          </select>
        </div>
        <div class="col-md-4">
          <label class="form-label">مدة التنبؤ</label>
          <select class="form-select" name="days">
            <option value="14">14 يوم</option>
            <option value="30">30 يوم</option>
          </select>
        </div>
      </div>
      <button class="btn btn-primary w-100" type="submit">ابدأ التحليل</button>
    </form>
  </div>

  {% if summary %}
  <div class="card mt-4 p-3">
    <h5>📋 ملخص أولي (مجاني)</h5>
    <p>المدينة: <strong>{{city}}</strong> — نوع التحليل: <strong>{{mode}}</strong></p>
    <p>عدد العينات المأخوذة: <strong>{{count}}</strong></p>
    <p>متوسط السعر (تقريبي): <strong>{{avg_price:,}} ريال</strong></p>
    <div><img src="data:image/png;base64,{{chart}}" class="img-fluid"></div>

    <hr>
    <p>هل تريدين التقرير الكامل والتوصيات والتنبؤات؟ اختاري باقة الدفع المناسبة:</p>
    <form method="post" action="/pay">
      <input type="hidden" name="token" value="{{token}}">
      <input type="hidden" name="mode" value="{{mode}}">
      <div class="d-grid gap-2">
        <button class="btn btn-success" name="price" value="{{price_quick}}">ادفع {{price_quick}} $ — باقة سريعة</button>
        <button class="btn btn-info" name="price" value="{{price_deep}}">ادفع {{price_deep}} $ — باقة دقيقة</button>
        <button class="btn btn-warning" name="price" value="{{price_vip}}">ادفع {{price_vip}} $ — باقة VIP (مخصصة)</button>
      </div>
    </form>
    <p class="mt-2 text-muted">ملحوظة: الدفع في وضع الاختبار (Sandbox). بعد الدفع سيظهر لك التقرير الكامل مع زر لتنزيل PDF.</p>
  </div>
  {% endif %}

</div>
</body>
</html>
"""

REPORT_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>تقريرك - وردة العقارية</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style> body { background:#f8fafc; } .card { direction:rtl; } </style>
</head>
<body>
<div class="container py-4">
  <h2 class="text-center mb-3">✅ تم الدفع بنجاح — تقريرك جاهز</h2>
  <div class="card p-3">
    <h5>📄 ملخص التقرير</h5>
    <p>المدينة: <strong>{{city}}</strong></p>
    <p>نوع التحليل: <strong>{{mode}}</strong></p>
    <p>عدد العينات: <strong>{{count}}</strong></p>
    <p>متوسط السعر: <strong>{{avg_price:,}} ريال</strong></p>
    <p>دقة النموذج: <strong>{{r2:.2f}}</strong> | متوسط الخطأ: <strong>{{mae:.0f}} ريال</strong></p>
    <hr>
    <h6>📊 التنبؤات القادمة</h6>
    <table class="table table-striped">
      <thead><tr><th>يوم</th><th>السعر المتوقع (ريال)</th></tr></thead>
      <tbody>
        {% for row in future %}
        <tr><td>{{loop.index}}</td><td>{{row['predicted_price']|round(0)}}</td></tr>
        {% endfor %}
      </tbody>
    </table>
    <div class="mt-3">
      <a class="btn btn-outline-primary" href="/download/{{token}}">⬇️ تنزيل التقرير PDF</a>
      <a class="btn btn-secondary" href="/">عودة للصفحة الرئيسية</a>
    </div>
  </div>
</div>
</body>
</html>
"""

# إعدادات الأسعار (دولار)
PRICE_QUICK = 99     # باقة سريعة
PRICE_DEEP = 499     # باقة دقيقة
PRICE_VIP  = 999     # باقة مميزة VIP

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HOME_HTML)

@app.route("/analyze", methods=["POST"])
def analyze():
    city = request.form.get("city", "الرياض")
    mode = request.form.get("mode", "quick")
    days = int(request.form.get("days", 14))

    # جلب البيانات (مجرّد تحليل سطحي أولي)
    df = fetch_properties(city, mode if mode in ["quick","deep"] else "deep")
    if df is None or df.empty:
        # فشل جلب أي بيانات
        return render_template_string(HOME_HTML, summary=False, city=city)

    avg_price = int(df["price"].mean()) if "price" in df.columns and not df.empty else 0
    count = len(df)

    # رسم histogram في صورة base64
    plt.figure(figsize=(8,3.5))
    plt.hist(df["price"], bins=20, edgecolor="black")
    plt.xlabel("السعر (ريال)")
    plt.tight_layout()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    chart_b64 = base64.b64encode(img_buf.read()).decode("utf-8")

    # إنشاء توكن مؤقت وحفظ النتائج
    token = str(uuid.uuid4())
    ANALYSES[token] = {
        "city": city,
        "mode": mode,
        "days": days,
        "df_records": df.to_dict(orient="records"),
        "avg_price": avg_price
    }

    # السعر المعروض في الأزرار (الدفع بالدولار)
    return render_template_string(HOME_HTML, summary=True, city=city, mode=mode,
                                  count=count, avg_price=avg_price, chart=chart_b64,
                                  token=token, price_quick=PRICE_QUICK, price_deep=PRICE_DEEP, price_vip=PRICE_VIP)

@app.route("/pay", methods=["POST"])
def pay():
    if not (PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET):
        return "⚠️ الدفع غير مفعّل. لم يتم إعداد مفاتيح PayPal في ملف .env."

    token = request.form.get("token")
    price = request.form.get("price")
    mode = request.form.get("mode", "quick")
    if not token or not price:
        return "⚠️ خطأ: لم نتمكن من إنشاء عملية الدفع."

    # خلق عملية دفع بايبال
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for("execute", _external=True),
            "cancel_url": url_for("home", _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "تقرير تحليل عقاري - وردة",
                    "sku": "report",
                    "price": str(price),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {"total": str(price), "currency": "USD"},
            "description": f"تحليل عقاري (نوع: {mode})",
            "custom": token  # نمرّر التوكن كي نربط عملية الدفع بنتيجتنا المؤقتة
        }]
    })

    if payment.create():
        # العثور على رابط الموافقة
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return redirect(approval_url)
        return "لم نستطع العثور على رابط الموافقة."
    else:
        return f"فشل إنشاء الدفع: {payment.error}"

@app.route("/execute")
def execute():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    if not payment_id or not payer_id:
        return "تم إلغاء الدفع أو لم يتم تقديم معلومات الدفع."

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # استخرج التوكن (custom) من معاملة بايبال
        try:
            token = None
            # payment.to_dict() للحصول على البنية الخام
            p_dict = payment.to_dict()
            if "transactions" in p_dict and len(p_dict["transactions"])>0:
                token = p_dict["transactions"][0].get("custom")
        except Exception:
            token = None

        if not token or token not in ANALYSES:
            # لا نجد التحليل المؤقت — لكن الدفع تم؛ نرجع رسالة مناسبة
            return "✅ تم الدفع بنجاح، لكن لم نتمكن من العثور على نتيجة التحليل (التحقق لاحقاً)."

        # تجهيز التقرير النهائي
        analysis = ANALYSES.pop(token)
        df = pd.DataFrame(analysis["df_records"])
        # تدريب النموذج
        model, poly, metrics = train_price_predictor(df)
        future = []
        if model is not None:
            future_df = predict_future_prices(model, poly, df, days=analysis.get("days",14))
            future = future_df.to_dict(orient="records")
        else:
            future = []

        # إنشاء PDF وأدخاله في الذاكرة
        pdf_bytes = create_pdf_report(analysis, future, metrics)
        # خزن الـ pdf مؤقتاً برمز جديد لكي يتم تنزيله
        REPORT_TOKEN = str(uuid.uuid4())
        ANALYSES[REPORT_TOKEN] = {
            "pdf": pdf_bytes,
            "city": analysis["city"],
            "mode": analysis["mode"],
            "avg_price": analysis["avg_price"],
            "count": len(df),
            "metrics": metrics,
            "future": future
        }

        # عرض صفحة نجاح + رابط تنزيل (نستخدم REPORT_TOKEN)
        return render_template_string(REPORT_HTML,
                                      city=analysis["city"],
                                      mode=analysis["mode"],
                                      count=len(df),
                                      avg_price=analysis["avg_price"],
                                      r2=metrics["r2"] if metrics else 0,
                                      mae=metrics["mae"] if metrics else 0,
                                      future=future,
                                      token=REPORT_TOKEN)
    else:
        return f"فشل تنفيذ الدفع: {payment.error}"

def create_pdf_report(analysis, future, metrics):
    """
    ينشئ PDF في الذاكرة ويعيد bytes
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    x_margin = 40
    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y, "تقرير التحليل العقاري — وردة العقارية")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(x_margin, y, f"المدينة: {analysis['city']}    النوع: {analysis['mode']}")
    y -= 20
    c.drawString(x_margin, y, f"عدد العينات: {len(analysis['df_records'])}    متوسط السعر: {analysis['avg_price']:,} ريال")
    y -= 30

    c.drawString(x_margin, y, "أداء نموذج التنبؤ:")
    y -= 20
    if metrics:
        c.drawString(x_margin, y, f"R2 = {metrics.get('r2',0):.3f}    MAE = {metrics.get('mae',0):.0f} ريال")
    else:
        c.drawString(x_margin, y, "البيانات غير كافية لتدريب نموذج التنبؤ.")
    y -= 30
    c.drawString(x_margin, y, "التنبؤات القادمة:")
    y -= 20
    if future:
        for i, row in enumerate(future[:20]):
            c.drawString(x_margin, y, f"يوم {i+1}: {int(row['predicted_price']):,} ريال")
            y -= 15
            if y < 80:
                c.showPage()
                y = height - 60
    else:
        c.drawString(x_margin, y, "لا توجد تنبؤات متاحة.")
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()

@app.route("/download/<report_token>")
def download(report_token):
    rec = ANALYSES.get(report_token)
    if not rec:
        return "❌ لا يوجد تقرير جاهز بهذا الرمز."
    pdf_bytes = rec.get("pdf")
    if not pdf_bytes:
        return "❌ لا يوجد PDF للتنزيل."
    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf",
                     as_attachment=True, download_name=f"report_{report_token}.pdf")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
