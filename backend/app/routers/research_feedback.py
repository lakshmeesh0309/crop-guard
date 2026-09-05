"""
Research Lab Feedback Loop — Section 4
Stores MobileNet + Groq experimental analysis feedback from farmers.
Provides admin analytics on prediction quality.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
from app.auth import get_current_user
from app.database import get_db
from bson import ObjectId
import hashlib

router = APIRouter(prefix="/research-feedback", tags=["Research Feedback"])


class FeedbackSubmit(BaseModel):
    crop: str
    image_hash: str                   # SHA-256 of the uploaded image bytes
    mobilenet_predictions: List[dict]  # top-5 MobileNet outputs
    groq_conclusion: str               # Groq experimental conclusion text
    feedback: str                      # "helpful" | "not_helpful"


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/")
async def submit_feedback(body: FeedbackSubmit, user=Depends(get_current_user)):
    """Store farmer feedback on a Research Lab experimental analysis."""
    if body.feedback not in ("helpful", "not_helpful"):
        raise HTTPException(400, "feedback must be 'helpful' or 'not_helpful'")

    db = get_db()
    await db["research_feedback"].insert_one({
        "user_id": str(user["_id"]),
        "crop": body.crop,
        "image_hash": body.image_hash,
        "mobilenet_predictions": body.mobilenet_predictions,
        "groq_conclusion": body.groq_conclusion,
        "feedback": body.feedback,
        "created_at": datetime.now(timezone.utc)
    })
    return {"success": True, "message": "Thank you for your feedback."}


@router.get("/analytics")
async def get_feedback_analytics(user=Depends(get_current_user)):
    """Admin-only analytics: feedback trends, misclassified crops, Groq correction frequency."""
    if not user.get("is_admin"):
        raise HTTPException(403, "Admin access required")

    db = get_db()

    # Total feedback counts
    total = await db["research_feedback"].count_documents({})
    helpful = await db["research_feedback"].count_documents({"feedback": "helpful"})
    not_helpful = await db["research_feedback"].count_documents({"feedback": "not_helpful"})

    # Top crops with not_helpful feedback (potential misclassification hotspots)
    pipeline_crops = [
        {"$match": {"feedback": "not_helpful"}},
        {"$group": {"_id": "$crop", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    cursor = db["research_feedback"].aggregate(pipeline_crops)
    top_misclassified = await cursor.to_list(length=10)

    # Feedback trend over last 30 days (grouped by day)
    pipeline_trend = [
        {"$group": {
            "_id": {
                "year": {"$year": "$created_at"},
                "month": {"$month": "$created_at"},
                "day": {"$dayOfMonth": "$created_at"}
            },
            "helpful": {"$sum": {"$cond": [{"$eq": ["$feedback", "helpful"]}, 1, 0]}},
            "not_helpful": {"$sum": {"$cond": [{"$eq": ["$feedback", "not_helpful"]}, 1, 0]}}
        }},
        {"$sort": {"_id.year": -1, "_id.month": -1, "_id.day": -1}},
        {"$limit": 30}
    ]
    cursor2 = db["research_feedback"].aggregate(pipeline_trend)
    trend = await cursor2.to_list(length=30)

    return {
        "total_feedback": total,
        "helpful": helpful,
        "not_helpful": not_helpful,
        "helpfulness_rate": round((helpful / total * 100), 1) if total > 0 else 0,
        "top_misclassified_crops": [
            {"crop": r["_id"], "count": r["count"]} for r in top_misclassified
        ],
        "daily_trend": [
            {
                "date": f"{r['_id']['year']}-{r['_id']['month']:02d}-{r['_id']['day']:02d}",
                "helpful": r["helpful"],
                "not_helpful": r["not_helpful"]
            }
            for r in trend
        ]
    }
