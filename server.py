# FastAPI server — يستقبل الإشارات ويعرضها للموقع
# uvicorn server:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Signal(BaseModel):
    time: str
    pair: str
    direction: str
    success_rate: float
    payout: float
    martingale: int
    trend_strength: Optional[int] = 0

class Payload(BaseModel):
    generated_at: Optional[str] = None
    signals: List[Signal]

STATE: Payload = Payload(signals=[])

@app.post("/signals")
def push(p: Payload):
    global STATE
    STATE = p
    return {"ok": True, "count": len(p.signals)}

@app.get("/")

def get():
    return STATE
