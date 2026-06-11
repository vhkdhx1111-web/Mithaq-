@app.get("/")
def get():
    global STATE
    
    # إذا كانت القائمة فارغة، نعيد الهيكلين فارغين تجنباً للأخطاء
    if not STATE.signals:
        return {
            "total": 0, "call_count": 0, "put_count": 0, "avg_win_rate": "0%", 
            "list": "", "signals": [], "total_signals": 0
        }
    
    # تجهيز قواميس وقوائم موازية لضمان قراءة الواجهة بأي صيغة مبرمجة بها
    formatted_list = []
    call_count = 0
    put_count = 0
    rates = []
    
    output_lines = [
        "⏰ TIMEZONE: UTC +6:00",
        "⋅◈ ⋅ ⏲️ 1 MINUTE WINDOW ⋅◈⋅",
        "⚙️ 1-STEP MARTINGALE INCLUDED",
        ""
    ]
    
    for sig in STATE.signals:
        # تحويل المتغيرات للصيغتين الاحتياطيتين (direction و action)
        action = sig.direction.upper() if hasattr(sig, 'direction') else "CALL"
        pair_name = sig.pair if hasattr(sig, 'pair') else "EUR/USD_OTC"
        sig_time = sig.time if hasattr(sig, 'time') else "00:00"
        rate = sig.success_rate if hasattr(sig, 'success_rate') else 80.0
        
        if action == "CALL":
            call_count += 1
        else:
            put_count += 1
            
        rates.append(rate)
        output_lines.append(f"M1; {pair_name}; {sig_time}; {action}")
        
        # بناء كائن متكامل يحتوي على كل المسميات المحتملة للواجهة
        formatted_list.append({
            "time": sig_time,
            "pair": pair_name,
            "direction": action,
            "action": action,
            "success_rate": rate,
            "win_rate": rate,
            "payout": sig.payout,
            "martingale": sig.martingale
        })
        
    avg_rate = sum(rates) // len(rates) if rates else 0
    
    # نعيد قاموساً ضخماً يحتوي على كل ردود الأفعال المتوقعة من الواجهة الزرقاء
    return {
        "total": len(STATE.signals),
        "total_signals": len(STATE.signals),
        "call_count": call_count,
        "put_count": put_count,
        "avg_win_rate": f"{avg_rate}%",
        "list": "\n".join(output_lines),
        "signals": formatted_list
    }
