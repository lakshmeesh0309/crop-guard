from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone, timedelta, date
from app.auth import get_current_user, serialize_user
from app.database import users_col, scans_col
from bson import ObjectId

IST = timezone(timedelta(hours=5, minutes=30))

router = APIRouter(prefix="/users", tags=["Users"])


class UserUpdate(BaseModel):
    name:      Optional[str] = None
    farm_name: Optional[str] = None
    location:  Optional[str] = None
    crops:     Optional[List[str]] = None


@router.get("/me")
async def get_profile(user=Depends(get_current_user)):
    return serialize_user(user)


@router.put("/me")
async def update_profile(body: UserUpdate, user=Depends(get_current_user)):
    col    = users_col()
    update = {k: v for k, v in body.model_dump().items() if v is not None}
    update["updated_at"] = datetime.now(timezone.utc)
    await col.update_one({"_id": user["_id"]}, {"$set": update})
    return {"success": True, "message": "Profile updated"}


@router.get("/me/stats")
async def get_stats(user=Depends(get_current_user)):
    col       = scans_col()
    uid       = str(user["_id"])
    all_scans = await col.find({"user_id": uid}).to_list(length=None)
    today_ist = datetime.now(IST).date()

    today_s  = [s for s in all_scans if s.get("created_at") and
                 s["created_at"].replace(tzinfo=timezone.utc).astimezone(IST).date() == today_ist]
    diseased = [s for s in all_scans if s.get("status") == "diseased"]
    healthy  = [s for s in all_scans if s.get("status") == "healthy"]
    confs    = [s.get("confidence", 0) for s in all_scans]

    return {
        "scans_today":    len(today_s),
        "diseases_found": len(diseased),
        "avg_confidence": round(sum(confs) / len(confs), 1) if confs else 0,
        "healthy_count":  len(healthy),
        "total_scans":    len(all_scans),
    }
