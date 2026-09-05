from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from app.auth import get_current_user
from app.database import get_db
from app.config import settings
from app.services.prediction import predict_disease
import uuid
import os
import time
import asyncio
from datetime import datetime, timezone

router = APIRouter(prefix="/diagnose", tags=["Diagnostics"])
ALLOWED = {"image/jpeg", "image/png", "image/webp", "image/jpg"}

# Official CropGuard v13 supported crops
OFFICIAL_CROPS = {"Tomato", "Potato", "Chilli", "Maize", "Rice", "Cotton", "Groundnut"}

async def run_diagnostic_pipeline_async(job_id: str, image_bytes: bytes, crop: str, field: str, language: str, user: dict):
    db = get_db()
    start_total = time.time()
    
    # 1. [UPLOAD] & Image Preprocessing
    t_start = time.time()
    await db["jobs"].update_one({"_id": job_id}, {"$set": {"status": "uploading"}})
    
    processed_bytes = image_bytes
    try:
        import io
        from PIL import Image
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        # Resize if width or height is larger than 1024px to optimize Gemini request size
        if img.width > 1024 or img.height > 1024:
            img.thumbnail((1024, 1024))
            out_buf = io.BytesIO()
            img.save(out_buf, format="JPEG", quality=85)
            processed_bytes = out_buf.getvalue()
            print(f"[PREPROCESSING] Compressed image from {len(image_bytes)} to {len(processed_bytes)} bytes")
    except Exception as ex:
        print(f"[PREPROCESSING] Image optimization failed: {ex}")
    
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(processed_bytes)
        
    t_upload = round((time.time() - t_start) * 1000, 1)
    print(f"[UPLOAD] {t_upload}ms")
    
    # 2. [GEMINI] & [WEATHER] running in parallel
    await db["jobs"].update_one({"_id": job_id}, {"$set": {"status": "analyzing"}})
    
    async def get_gemini_report():
        t_gem_start = time.time()
        # predict_disease already filters candidate diseases by selected crop!
        pred = await predict_disease(processed_bytes, crop, language)
        return pred, t_gem_start
        
    async def get_weather():
        try:
            from app.routers.weather import get_weather_for_city
            return await get_weather_for_city("Visakhapatnam")
        except Exception:
            return None
            
    try:
        # Execute vision prediction and weather retrieval concurrently
        results = await asyncio.gather(
            get_gemini_report(),
            get_weather(),
            return_exceptions=True
        )
        
        # Handle predictions exceptions
        if isinstance(results[0], Exception):
            raise results[0]
            
        pred, t_gem_start = results[0]
        weather_data = results[1] if not isinstance(results[1], Exception) else None
        
        t_gemini_time = round((time.time() - t_gem_start) * 1000, 1)
        print(f"[GEMINI] {t_gemini_time}ms")
        
    except Exception as e:
        print(f"[BACKGROUND DIAGNOSE ERROR] {e}")
        await db["jobs"].update_one({"_id": job_id}, {
            "$set": {
                "status": "failed",
                "error": "Diagnosis temporarily unavailable. Please try again shortly."
            }
        })
        return

    # 3. [RAG] Retrieval (Filtered by selected crop)
    await db["jobs"].update_one({"_id": job_id}, {"$set": {"status": "retrieving_knowledge"}})
    t_rag_start = time.time()
    
    if pred.get("disease") and "healthy" not in pred["disease"].lower():
        t_col = db["treatments"]
        # Filter by selected crop specifically to minimize latency
        treatment = await t_col.find_one({
            "crops": crop,
            "disease": {"$regex": pred["disease"], "$options": "i"}
        })
        if not treatment:
            # Fallback global query
            treatment = await t_col.find_one({"disease": {"$regex": pred["disease"], "$options": "i"}})
            
        if treatment:
            treatment["id"] = str(treatment.pop("_id"))
            pred["treatment"] = treatment
        else:
            pred["treatment"] = None
    else:
        pred["treatment"] = None
        
    t_rag = round((time.time() - t_rag_start) * 1000, 1)
    print(f"[RAG] {t_rag}ms")

    # 4. [WEATHER] Analysis Context binding
    await db["jobs"].update_one({"_id": job_id}, {"$set": {"status": "weather_analysis"}})
    t_weather_start = time.time()
    
    if weather_data:
        pred["weather_advisory"] = {
            "temp": weather_data.get("temp"),
            "humidity": weather_data.get("humidity"),
            "wind": weather_data.get("wind"),
            "description": weather_data.get("description"),
            "recommendation": "High humidity - inspect fields soon." if weather_data.get("humidity", 0) > 75 else "Dry conditions."
        }
    else:
        pred["weather_advisory"] = None
        
    t_weather = round((time.time() - t_weather_start) * 1000, 1)
    print(f"[WEATHER] {t_weather}ms")

    # 5. [REPORT] Generation
    await db["jobs"].update_one({"_id": job_id}, {"$set": {"status": "generating_report"}})
    t_report_start = time.time()
    
    scan_document = {
        "user_id": str(user["_id"]),
        "disease": pred["disease"],
        "crop": crop,
        "confidence": pred["confidence"],
        "severity": pred["severity"],
        "severity_label": pred["severity_label"],
        "spread_risk": pred["spread_risk"],
        "urgency": pred["urgency"],
        "risk_score": pred["risk_score"],
        "pathogen": pred["pathogen"],
        
        "ai_engine": pred["ai_engine"],
        "mobilenet_crop_prediction": pred["mobilenet_crop_prediction"],
        "mobilenet_top5": pred["mobilenet_top5"],
        
        "image_path": filename,
        "field_name": field,
        "treatment_summary": pred["treatment"]["steps"][0]["description"] if (pred.get("treatment") and pred["treatment"].get("steps")) else pred.get("treatment_summary", "Monitor crop daily."),
        "weather_notes": pred["weather_advisory"]["recommendation"] if pred.get("weather_advisory") else None,
        
        "generated_report": pred["generated_report"],
        "language": language,
        "created_at": datetime.utcnow()
    }
    
    t_report = round((time.time() - t_report_start) * 1000, 1)
    print(f"[REPORT] {t_report}ms")

    # 6. [MONGO] Storage
    t_mongo_start = time.time()
    inserted = await db["scans"].insert_one(scan_document)
    scan_id = str(inserted.inserted_id)
    scan_document["id"] = scan_id
    scan_document.pop("_id", None)
    
    t_mongo = round((time.time() - t_mongo_start) * 1000, 1)
    print(f"[MONGO] {t_mongo}ms")
    
    # Output total diagnostic timings
    total_time = round((time.time() - start_total) * 1000, 1)
    print(f"\n===== DIAGNOSTICS REPORT JOB {job_id} =====")
    print(f"[UPLOAD] {t_upload}ms")
    print(f"[GEMINI] {t_gemini_time}ms")
    print(f"[RAG] {t_rag}ms")
    print(f"[WEATHER] {t_weather}ms")
    print(f"[REPORT] {t_report}ms")
    print(f"[MONGO] {t_mongo}ms")
    print(f"Total processing latency: {total_time}ms\n==========================================")
    
    # Update job completion state
    await db["jobs"].update_one({"_id": job_id}, {
        "$set": {
            "status": "completed",
            "result": scan_document
        }
    })

    # Insert scan-complete notification for user
    try:
        disease_name = scan_document.get("disease", "Unknown")
        is_healthy = "healthy" in disease_name.lower()
        await db["notifications"].insert_one({
            "user_id": str(user["_id"]),
            "type": "scan_completed",
            "title": "Diagnosis Complete" if is_healthy else "Disease Detected",
            "message": f"Your {crop} leaf scan completed. {'No disease detected.' if is_healthy else f'{disease_name} identified.'}",
            "read": False,
            "created_at": datetime.now(timezone.utc)
        })
    except Exception as notif_err:
        print(f"[NOTIFY] Failed to create scan notification: {notif_err}")

@router.post("/")
async def create_diagnostic_job(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    crop: str = Form(...),
    field: str = Form(""),
    language: str = Form("en"),
    user=Depends(get_current_user)
):
    if crop not in OFFICIAL_CROPS:
        raise HTTPException(400, "This crop is currently outside CropGuard's verified diagnostic coverage.")

    if image.content_type not in ALLOWED:
        raise HTTPException(400, "File must be an image (JPG, PNG, WEBP)")
        
    contents = await image.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "Image must be under 10MB")
        
    job_id = str(uuid.uuid4())
    db = get_db()
    
    # Initialize the job in database
    await db["jobs"].insert_one({
        "_id": job_id,
        "status": "uploading",
        "created_at": datetime.utcnow()
    })
    
    # Run the diagnosis processing workflow in the background
    background_tasks.add_task(
        run_diagnostic_pipeline_async,
        job_id,
        contents,
        crop,
        field,
        language,
        user
    )
    
    return {
        "job_id": job_id,
        "status": "processing"
    }

@router.get("/status/{job_id}")
async def get_diagnostic_job_status(job_id: str, user=Depends(get_current_user)):
    db = get_db()
    job = await db["jobs"].find_one({"_id": job_id})
    if not job:
        raise HTTPException(404, "Job not found")
        
    # Serialize mongo document
    job["job_id"] = job.pop("_id")
    return job
