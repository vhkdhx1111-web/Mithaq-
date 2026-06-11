# ARIA TREDAR — Local Collector for Pocket Option OTC
# يُشغَّل محلياً ويرفع الإشارات الناتجة إلى الموقع عبر POST.
#
# pip install fastapi uvicorn pandas numpy requests
#
# 1) اجمع بيانات الشموع من Pocket Option (مكتبة غير رسمية أو CSV).
# 2) حلّل كل دقيقة على مدار آخر N يوم.
# 3) أنشئ قائمة الإشارات وفق نسبة النجاح وMartingale.
# 4) ارفعها إلى الـ FastAPI الخاص بك ثم اعرضها في الموقع.

import requests, json
from datetime import datetime

API_BASE = "http://localhost:8000"   # عدّل هذا لرابط FastAPI الخاص بك

def push(signals):
    r = requests.post(f"{API_BASE}/signals", json={
        "generated_at": datetime.utcnow().isoformat(),
        "signals": signals
    })
    print(r.status_code, r.text)

if __name__ == "__main__":
    sample = [
        {"time":"14:32","pair":"EURUSD-OTC","direction":"CALL",
         "success_rate":86.4,"payout":92,"martingale":0,"trend_strength":2},
        {"time":"14:45","pair":"AUDCAD-OTC","direction":"PUT",
         "success_rate":83.1,"payout":85,"martingale":1,"trend_strength":3},
    ]
    push(sample)
