"""
Admin Router — Platform-wide management endpoints.
All routes require admin role via get_admin_user dependency.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from app.auth import get_admin_user
from app.database import users_col, scans_col
from bson import ObjectId
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/admin", tags=["Admin"])


def _serialize_user(u):
    return {
        "id": str(u["_id"]),
        "name": u.get("name", ""),
        "email": u.get("email", ""),
        "role": u.get("role", "farmer"),
        "farm_name": u.get("farm_name", ""),
        "location": u.get("location", ""),
        "crops": u.get("crops", []),
        "created_at": u.get("created_at", ""),
        "deleted_at": u.get("deleted_at"),
    }


def _serialize_scan(s):
    return {
        "id": str(s["_id"]),
        "user_id": s.get("user_id", ""),
        "user_name": s.get("user_name", ""),
        "crop": s.get("crop", ""),
        "disease": s.get("disease", ""),
        "confidence": s.get("confidence", 0),
        "status": s.get("status", "pending"),
        "ai_source": s.get("ai_source", ""),
        "created_at": s.get("created_at", ""),
    }


# ─── Platform Stats ───────────────────────────────────
@router.get("/stats")
async def admin_stats(user=Depends(get_admin_user)):
    uc = users_col()
    sc = scans_col()

    total_users = await uc.count_documents({"deleted_at": {"$exists": False}})
    total_scans = await sc.count_documents({})
    total_diseased = await sc.count_documents({"status": "diseased"})

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    scans_today = await sc.count_documents({"created_at": {"$gte": today_start}})

    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    new_users_this_week = await uc.count_documents({"created_at": {"$gte": week_ago}})

    # Top diseases aggregation
    top_diseases_pipeline = [
        {"$match": {"disease": {"$ne": "Healthy"}}},
        {"$group": {"_id": "$disease", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]
    top_diseases = []
    async for doc in sc.aggregate(top_diseases_pipeline):
        top_diseases.append({"disease": doc["_id"], "count": doc["count"]})

    # Top crops aggregation
    top_crops_pipeline = [
        {"$group": {"_id": "$crop", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]
    top_crops = []
    async for doc in sc.aggregate(top_crops_pipeline):
        top_crops.append({"crop": doc["_id"], "count": doc["count"]})

    # Average confidence
    avg_pipeline = [
        {"$group": {"_id": None, "avg_conf": {"$avg": "$confidence"}}}
    ]
    avg_confidence = 0.0
    async for doc in sc.aggregate(avg_pipeline):
        avg_confidence = round(doc["avg_conf"] or 0, 1)

    # Model info
    try:
        from app.services.model_trainer import training_status
        model_version = training_status.get("version", "v1.0")
        model_accuracy = training_status.get("accuracy")
        last_trained = training_status.get("last_trained")
    except ImportError:
        model_version = "v1.0"
        model_accuracy = None
        last_trained = None

    return {
        "total_users": total_users,
        "total_scans": total_scans,
        "total_diseased": total_diseased,
        "scans_today": scans_today,
        "top_diseases": top_diseases,
        "top_crops": top_crops,
        "new_users_this_week": new_users_this_week,
        "avg_confidence_platform": avg_confidence,
        "model_version": model_version,
        "model_accuracy": model_accuracy,
        "last_trained": last_trained,
    }


# ─── User Management ──────────────────────────────────
@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_admin_user),
):
    uc = users_col()
    sc = scans_col()
    skip = (page - 1) * limit
    total = await uc.count_documents({"deleted_at": {"$exists": False}})

    users = []
    async for u in uc.find({"deleted_at": {"$exists": False}}).sort("created_at", -1).skip(skip).limit(limit):
        serialized = _serialize_user(u)
        serialized["scans_count"] = await sc.count_documents({"user_id": str(u["_id"])})
        users.append(serialized)

    return {"users": users, "total": total, "page": page, "limit": limit}


@router.get("/users/{user_id}")
async def get_user_detail(user_id: str, user=Depends(get_admin_user)):
    uc = users_col()
    sc = scans_col()

    try:
        target = await uc.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(404, "Invalid user ID")
    if not target:
        raise HTTPException(404, "User not found")

    serialized = _serialize_user(target)
    serialized["scans_count"] = await sc.count_documents({"user_id": user_id})

    # Fetch recent scans
    scans = []
    async for s in sc.find({"user_id": user_id}).sort("created_at", -1).limit(20):
        scans.append(_serialize_scan(s))
    serialized["recent_scans"] = scans

    return serialized


@router.patch("/users/{user_id}/role")
async def change_user_role(user_id: str, body: dict, user=Depends(get_admin_user)):
    role = body.get("role")
    if role not in ("farmer", "admin"):
        raise HTTPException(400, "Role must be 'farmer' or 'admin'")

    uc = users_col()
    try:
        result = await uc.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": role}})
    except Exception:
        raise HTTPException(404, "Invalid user ID")
    if result.matched_count == 0:
        raise HTTPException(404, "User not found")

    return {"message": f"User role updated to {role}"}


@router.delete("/users/{user_id}")
async def soft_delete_user(user_id: str, user=Depends(get_admin_user)):
    uc = users_col()
    try:
        result = await uc.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"deleted_at": datetime.now(timezone.utc)}}
        )
    except Exception:
        raise HTTPException(404, "Invalid user ID")
    if result.matched_count == 0:
        raise HTTPException(404, "User not found")

    return {"message": "User account disabled"}


# ─── All Scans ─────────────────────────────────────────
@router.get("/scans")
async def list_all_scans(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_admin_user),
):
    sc = scans_col()
    skip = (page - 1) * limit
    total = await sc.count_documents({})

    scans = []
    async for s in sc.find().sort("created_at", -1).skip(skip).limit(limit):
        scans.append(_serialize_scan(s))

    return {"scans": scans, "total": total, "page": page, "limit": limit}


# ─── Model Management ─────────────────────────────────
@router.get("/model/status")
async def model_status(user=Depends(get_admin_user)):
    try:
        from app.services.model_trainer import training_status
        return training_status
    except ImportError:
        return {
            "status": "idle",
            "progress": 0,
            "log": ["Model trainer module not available"],
            "version": "v1.0",
            "accuracy": None,
            "last_trained": None,
            "dataset": "PlantVillage (Kaggle)",
            "error": None,
        }


@router.post("/model/trigger-training")
async def trigger_training(user=Depends(get_admin_user)):
    import asyncio

    try:
        from app.services.model_trainer import training_status, run_training
    except ImportError:
        raise HTTPException(500, "Model trainer module not available")

    from app.config import settings

    if training_status["status"] in ("training", "downloading"):
        raise HTTPException(400, "Training is already in progress")
    if not settings.KAGGLE_USERNAME or not settings.KAGGLE_KEY:
        raise HTTPException(400, "KAGGLE_USERNAME and KAGGLE_KEY must be set in .env to trigger training")

    # Reset status
    training_status.update({
        "status": "downloading",
        "progress": 0,
        "log": [],
        "error": None,
    })

    # Fire and forget
    asyncio.create_task(run_training(settings.KAGGLE_USERNAME, settings.KAGGLE_KEY))
    return {"message": "Training started", "status": "downloading"}


# ─── Extended Analytics ───────────────────────────────
@router.get("/analytics")
async def admin_analytics(user=Depends(get_admin_user)):
    sc = scans_col()
    
    # 1. Total scans
    total_scans = await sc.count_documents({})
    
    # 2. Disease trends
    disease_pipeline = [
        {"$group": {"_id": "$disease", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    disease_trends = []
    async for d in sc.aggregate(disease_pipeline):
        disease_trends.append({"name": d["_id"], "value": d["count"]})
        
    # 3. Crop distribution
    crop_pipeline = [
        {"$group": {"_id": "$crop", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    crop_distribution = []
    async for c in sc.aggregate(crop_pipeline):
        crop_distribution.append({"name": c["_id"], "value": c["count"]})
        
    # 4. Evidence quality distribution
    evidence_pipeline = [
        {"$group": {"_id": {"$ifNull": ["$generated_report.overall_evidence_strength", "Low"]}, "count": {"$sum": 1}}}
    ]
    evidence_dist = []
    async for e in sc.aggregate(evidence_pipeline):
        evidence_dist.append({"name": e["_id"], "value": e["count"]})
        
    # 5. Engine usage
    engine_pipeline = [
        {"$group": {"_id": {"$ifNull": ["$ai_engine", "Local Fallback"]}, "count": {"$sum": 1}}}
    ]
    engine_usage = []
    async for eng in sc.aggregate(engine_pipeline):
        engine_usage.append({"name": eng["_id"], "value": eng["count"]})
        
    # 6. MobileNet Research Analytics
    crop_match_count = await sc.count_documents({
        "mobilenet_crop_prediction": {"$exists": True, "$ne": None},
        "$expr": {"$eq": ["$mobilenet_crop_prediction", "$crop"]}
    })
    
    mismatches_cursor = sc.find({
        "mobilenet_crop_prediction": {"$exists": True, "$ne": None},
        "$expr": {"$ne": ["$mobilenet_crop_prediction", "$crop"]}
    }).sort("created_at", -1).limit(10)
    mismatches = []
    async for m in mismatches_cursor:
        mismatches.append({
            "id": str(m["_id"]),
            "user_crop": m.get("crop"),
            "mobilenet_crop": m.get("mobilenet_crop_prediction"),
            "disease": m.get("disease"),
            "created_at": m.get("created_at")
        })
        
    # 7. Monthly activity (last 6 months)
    monthly_pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"}
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
        {"$limit": 6}
    ]
    monthly_activity = []
    async for m_act in sc.aggregate(monthly_pipeline):
        yr = m_act["_id"]["year"]
        mth = m_act["_id"]["month"]
        monthly_activity.append({"month": f"{yr}-{mth:02d}", "scans": m_act["count"]})
        
    return {
        "total_scans": total_scans,
        "disease_trends": disease_trends,
        "crop_distribution": crop_distribution,
        "evidence_distribution": evidence_dist,
        "engine_usage": engine_usage,
        "mobilenet_research": {
            "crop_match_count": crop_match_count,
            "mismatches": mismatches
        },
        "monthly_activity": monthly_activity
    }
