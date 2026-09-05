from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timezone
from app.auth import get_current_user
from app.database import notifications_col, users_col
from bson import ObjectId

router = APIRouter(prefix="/notifications", tags=["Notifications"])

class PreferencesUpdate(BaseModel):
    weather_alerts: bool
    disease_alerts: bool
    scan_alerts: bool
    treatment_reminders: bool

def serialize_notification(n: dict) -> dict:
    n["id"] = str(n.pop("_id"))
    return n

@router.get("/")
async def list_notifications(user=Depends(get_current_user)):
    col = notifications_col()
    cursor = col.find({"user_id": str(user["_id"])}).sort("created_at", -1).limit(50)
    notifications = await cursor.to_list(length=50)
    return [serialize_notification(n) for n in notifications]

@router.patch("/{id}/read")
async def mark_read(id: str, user=Depends(get_current_user)):
    col = notifications_col()
    result = await col.update_one(
        {"_id": ObjectId(id), "user_id": str(user["_id"])},
        {"$set": {"read": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Notification not found")
    return {"success": True}

@router.patch("/read-all")
async def mark_all_read(user=Depends(get_current_user)):
    col = notifications_col()
    await col.update_many(
        {"user_id": str(user["_id"]), "read": False},
        {"$set": {"read": True}}
    )
    return {"success": True}

@router.get("/preferences")
async def get_preferences(user=Depends(get_current_user)):
    # Fallback default values
    defaults = {
        "weather_alerts": True,
        "disease_alerts": True,
        "scan_alerts": True,
        "treatment_reminders": True
    }
    prefs = user.get("notification_preferences", defaults)
    return prefs

@router.put("/preferences")
async def save_preferences(body: PreferencesUpdate, user=Depends(get_current_user)):
    u_col = users_col()
    await u_col.update_one(
        {"_id": user["_id"]},
        {"$set": {"notification_preferences": body.dict()}}
    )
    return {"success": True}
