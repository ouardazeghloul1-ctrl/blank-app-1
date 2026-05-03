from fastapi import FastAPI, Request
import uvicorn
import uuid
import os

app = FastAPI()

@app.post("/webhook")
async def lemon_webhook(request: Request):
    data = await request.json()

    event = data.get("meta", {}).get("event_name")

    if event == "order_created":
        email = data["data"]["attributes"]["user_email"]

        # 🔥 هنا تنشئين التقرير
        filename = f"{uuid.uuid4()}.pdf"
        filepath = f"reports/{filename}"

        os.makedirs("reports", exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(b"Dummy PDF content")  # لاحقاً نربطه بتقريرك الحقيقي

        print(f"Report created for {email}")

    return {"status": "ok"}
