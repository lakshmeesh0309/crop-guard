from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.database import scans_col
from datetime import date, datetime, timezone, timedelta
from collections import defaultdict

IST = timezone(timedelta(hours=5, minutes=30))

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def dashboard(user=Depends(get_current_user)):
    col       = scans_col()
    uid       = str(user["_id"])
    all_scans = await col.find({"user_id": uid}).to_list(length=None)
    today_ist = datetime.now(IST).date()

    today_s  = [s for s in all_scans if s.get("created_at") and
                 s["created_at"].replace(tzinfo=timezone.utc).astimezone(IST).date() == today_ist]
    diseased = [s for s in all_scans if s.get("status") == "diseased"]
    healthy  = [s for s in all_scans if s.get("status") == "healthy"]
    confs    = [s.get("confidence", 0) for s in all_scans]

    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    week_counts = {d: 0 for d in days}
    for s in all_scans:
        dt = s.get("created_at")
        if dt:
            try:
                day_key = dt.strftime("%a")
                if day_key in week_counts:
                    week_counts[day_key] += 1
            except Exception:
                pass

    disease_counts = defaultdict(int)
    for s in diseased:
        disease_counts[s.get("disease","Unknown")] += 1
    top_diseases = [{"disease":d,"count":c} for d,c in sorted(disease_counts.items(), key=lambda x:-x[1])[:5]]

    crop_risk_raw = defaultdict(list)
    for s in all_scans:
        crop_risk_raw[s.get("crop","Unknown")].append(s.get("spread_risk", 0))
    crop_risk = {k: round(sum(v)/len(v)) for k,v in crop_risk_raw.items()}

    return {
        "scans_today":    len(today_s),
        "diseases_found": len(diseased),
        "avg_confidence": round(sum(confs)/len(confs),1) if confs else 0,
        "healthy_count":  len(healthy),
        "total_scans":    len(all_scans),
        "week_counts":    week_counts,
        "top_diseases":   top_diseases,
        "crop_risk":      crop_risk,
    }
