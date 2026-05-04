from fastapi import FastAPI, Request
import uuid
import os

app = FastAPI()

# ✅ route رئيسي للتأكد أن السيرفر يعمل
@app.get("/")
def home():
    return {"message": "Warda backend is working"}

# ✅ webhook من Lemon Squeezy
@app.post("/webhook")
async def lemon_webhook(request: Request):
    data = await request.json()

    event = data.get("meta", {}).get("event_name")

    if event == "order_created":
        email = data.get("data", {}).get("attributes", {}).get("user_email")

        # إنشاء ملف PDF وهمي (مؤقت)
        filename = f"{uuid.uuid4()}.pdf"
        filepath = f"reports/{filename}"

        os.makedirs("reports", exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(b"Dummy PDF content")

        print(f"Report created for {email}")

    return {"status": "ok"}
