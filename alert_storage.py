# alert_storage.py
import json
from datetime import datetime
from pathlib import Path

FILE = Path("alerts/alerts_db.json")

def load_alerts():
    if not FILE.exists():
        return []
    return json.loads(FILE.read_text(encoding="utf-8"))

def save_alert(alert: dict):
    alerts = load_alerts()
    alert["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerts.append(alert)
    FILE.write_text(
        json.dumps(alerts, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_today_alerts(city: str):
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        a for a in load_alerts()
        if a["city"] == city and a["generated_at"].startswith(today)
    ]
