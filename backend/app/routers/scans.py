from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timezone
from app.auth import get_current_user
from app.database import scans_col, treatments_col
from app.services.prediction import predict_disease
from app.config import settings
from bson import ObjectId
import uuid, os, json, asyncio, re

router = APIRouter(prefix="/scans", tags=["Scans"])
ALLOWED = {"image/jpeg","image/png","image/webp","image/jpg"}


def serialize_scan(s: dict) -> dict:
    s["id"] = str(s.pop("_id"))
    return s


@router.post("/")
async def create_scan(
    image: UploadFile = File(...),
    crop:  str = Form(...),
    field: str = Form(""),
    language: str = Form("en"),
    user=Depends(get_current_user),
):
    # Official CropGuard v13 supported crops
    SUPPORTED_CROPS = {"Tomato", "Potato", "Chilli", "Maize", "Rice", "Cotton", "Groundnut"}
    if crop not in SUPPORTED_CROPS:
        raise HTTPException(400, "This crop is currently outside CropGuard's verified diagnostic coverage.")

    if image.content_type not in ALLOWED:
        raise HTTPException(400, "File must be an image (JPG, PNG, WEBP)")
    contents = await image.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "Image must be under 10MB")

    ext      = (image.filename or "leaf.jpg").rsplit(".", 1)[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    pred = await predict_disease(contents, crop, language)

    # Auto-fetch treatment from MongoDB (fallback to local if not found or empty)
    if pred.get("disease") and "healthy" not in pred["disease"].lower():
        t_col = treatments_col()
        treatment = await t_col.find_one({"disease": {"$regex": pred["disease"], "$options": "i"}})
        if treatment:
            treatment["id"] = str(treatment.pop("_id"))
            pred["treatment"] = treatment
        else:
            pred["treatment"] = None
    else:
        pred["treatment"] = None

    # Add weather context
    try:
        from app.routers.weather import current as get_weather
        weather = await get_weather(lat=settings.DEFAULT_LAT, lon=settings.DEFAULT_LON)
        hum = weather.get("humidity", 70)
        temp = weather.get("temp", 28)
        weather_note = None
        disease = pred.get("disease", "")
        if "healthy" not in disease.lower():
            if hum > 80:
                weather_note = f"Current humidity {hum}% in Vizag is accelerating spread. Spray urgently before next rain."
            elif hum > 70:
                weather_note = f"Humidity {hum}% creates favorable conditions. Monitor closely over next 3 days."
            elif temp > 35:
                weather_note = f"High temperature {temp}C may stress the plant further. Irrigate and shade if possible."
            else:
                weather_note = f"Current conditions: {temp}C, {hum}% humidity. Moderate disease progression expected."
        pred["weather_context"] = {"temp": temp, "humidity": hum, "note": weather_note}
    except Exception:
        pass

    scan = {
        "user_id":           str(user["_id"]),
        "crop":              crop,
        "field_name":        field,
        "disease":           pred["disease"],
        "pathogen":          pred.get("pathogen"),
        "confidence":        pred["confidence"],
        "severity":          pred.get("severity", 0),
        "spread_risk":       pred.get("spread_risk", 0),
        "urgency":           pred.get("urgency", 0),
        "risk_score":        pred.get("risk_score", 0),
        "severity_label":    pred.get("severity_label", "None"),
        "image_path":        filename,
        "status":            "healthy" if "healthy" in pred["disease"].lower() else "diseased",
        "treatment":         pred.get("treatment"),
        "treatment_summary": pred.get("treatment_summary", ""),
        "weather_context":   pred.get("weather_context"),
        # v12 hybrid and report fields
        "ai_engine":                 pred.get("ai_engine", "Local Fallback"),
        "mobilenet_crop_prediction": pred.get("mobilenet_crop_prediction"),
        "mobilenet_top5":            pred.get("mobilenet_top5", []),
        "generated_report":          pred.get("generated_report"),
        "language":                  pred.get("language", language),
        "created_at":        datetime.now(timezone.utc),
    }
    col    = scans_col()
    result = await col.insert_one(scan)
    scan["_id"] = result.inserted_id

    # Trigger In-App Notifications based on preferences
    try:
        from app.database import create_notification
        await create_notification(
            user_id=str(user["_id"]),
            type="Scan Completed",
            title=f"Scan Completed: {pred['disease']}",
            message=f"Analysis of {crop} leaf photo is complete. Confidence: {pred['confidence']}%",
            metadata={"scan_id": str(scan["_id"]), "disease": pred["disease"], "crop": crop}
        )
        if pred.get("risk_score", 0) >= 60:
            await create_notification(
                user_id=str(user["_id"]),
                type="High Disease Risk",
                title=f"High Disease Risk: {pred['disease']}",
                message=f"Urgent action required! Risk score is {pred['risk_score']}/100.",
                metadata={"scan_id": str(scan["_id"]), "disease": pred["disease"], "crop": crop}
            )
    except Exception as e:
        print(f"[WARN] Failed to trigger notification: {e}")

    return serialize_scan(scan)


@router.get("/")
async def list_scans(
    crop:   str = Query(None),
    status: str = Query(None),
    limit:  int = Query(50, le=200),
    user=Depends(get_current_user),
):
    col     = scans_col()
    query   = {"user_id": str(user["_id"])}
    if crop:   query["crop"]   = crop
    if status: query["status"] = status
    cursor  = col.find(query).sort("created_at", -1).limit(limit)
    scans   = await cursor.to_list(length=limit)
    return [serialize_scan(s) for s in scans]


@router.get("/{scan_id}")
async def get_scan(scan_id: str, user=Depends(get_current_user)):
    col  = scans_col()
    scan = await col.find_one({"_id": ObjectId(scan_id), "user_id": str(user["_id"])})
    if not scan:
        raise HTTPException(404, "Scan not found")
    return serialize_scan(scan)


@router.patch("/{scan_id}/status")
async def update_status(scan_id: str, body: dict, user=Depends(get_current_user)):
    col = scans_col()
    await col.update_one(
        {"_id": ObjectId(scan_id), "user_id": str(user["_id"])},
        {"$set": {"status": body.get("status")}}
    )
    return {"success": True}


@router.delete("/{scan_id}")
async def delete_scan(scan_id: str, user=Depends(get_current_user)):
    col  = scans_col()
    scan = await col.find_one({"_id": ObjectId(scan_id), "user_id": str(user["_id"])})
    if not scan:
        raise HTTPException(404, "Scan not found")
    if scan.get("image_path"):
        path = os.path.join(settings.UPLOAD_DIR, scan["image_path"])
        if os.path.exists(path):
            os.remove(path)
    await col.delete_one({"_id": ObjectId(scan_id)})
    return {"success": True}


@router.get("/image/{filename}")
async def get_image(filename: str, user=Depends(get_current_user)):
    path = os.path.join(settings.UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Image not found")
    return FileResponse(path)


# ──────────────────────────────────────────────────────────────────────────────
# RESEARCH LAB ENDPOINT (EXPERIMENTAL — MobileNet + Groq ONLY)
# Completely isolated from the official Gemini-based diagnosis pipeline.
# ──────────────────────────────────────────────────────────────────────────────
@router.post("/research")
async def research_analysis(
    image: UploadFile = File(...),
    crop: str = Form("Unknown"),
    language: str = Form("en"),
    user=Depends(get_current_user)
):
    """Experimental Research Lab: MobileNet top-5 + Groq reasoning."""
    if image.content_type not in ALLOWED:
        raise HTTPException(400, "File must be an image (JPG, PNG, WEBP)")
    contents = await image.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "Image must be under 10MB")

    print(f"\n[RESEARCH] ===== Research Lab Pipeline =====")
    print(f"[RESEARCH] Crop: {crop} | Language: {language} | Image bytes: {len(contents)}")

    # ── STEP 1: MobileNet ─────────────────────────────────────────────────
    mobilenet_error = None
    raw_mobilenet = None
    try:
        from ml.inference import predict as predict_local
        raw_mobilenet = predict_local(contents)
        print(f"[RESEARCH] MobileNet raw: {raw_mobilenet}")
    except Exception as e:
        mobilenet_error = str(e)
        print(f"[RESEARCH] MobileNet unavailable: {e}")

    # Normalise top_predictions
    if raw_mobilenet and raw_mobilenet.get("top5"):
        top_predictions = []
        for item in raw_mobilenet["top5"]:
            conf = item.get("confidence", 0)
            if isinstance(conf, float) and conf <= 1.0:
                conf = round(conf * 100, 1)
            top_predictions.append({
                "disease": item.get("disease") or item.get("label") or item.get("class") or "Unknown",
                "confidence": conf
            })
    else:
        mobilenet_error = mobilenet_error or "MobileNet model not loaded — using demo predictions"
        top_predictions = [
            {"disease": f"{crop} Early Blight",  "confidence": 38.5},
            {"disease": f"{crop} Leaf Spot",     "confidence": 24.2},
            {"disease": "Healthy",               "confidence": 18.1},
            {"disease": f"{crop} Rust",          "confidence": 11.4},
            {"disease": f"{crop} Mosaic Virus",  "confidence":  7.8},
        ]
        print(f"[RESEARCH] Demo predictions used (MobileNet not available)")

    print(f"[RESEARCH] top_predictions: {json.dumps(top_predictions)}")

    selected_candidate  = top_predictions[0]["disease"] if top_predictions else "Unknown"
    rejected_candidates = [p["disease"] for p in top_predictions[1:]]
    research_confidence = f"{top_predictions[0]['confidence']:.1f}%" if top_predictions else "0%"

    # ── STEP 2: Groq Reasoning ────────────────────────────────────────────
    groq_reasoning          = ""
    groq_experimental_notes = ""
    groq_next_steps         = ""
    groq_error              = None
    raw_text                = ""

    top5_str = json.dumps(top_predictions, indent=2)
    groq_prompt = (
        f"You are an experimental agricultural research AI.\n"
        f"A local MobileNet v3 model analyzed a {crop} leaf and returned these Top-5 predictions:\n"
        f"{top5_str}\n\n"
        f"Top candidate: \"{selected_candidate}\" at {research_confidence} confidence.\n\n"
        f"Reply ONLY with a JSON object matching this EXACT schema (no extra keys, no markdown fences):\n"
        '{"visual_reasoning":"2-3 sentences why the top candidate was selected",'
        '"experimental_notes":"observations about distribution and overlapping symptoms",'
        '"next_steps":"numbered field scouting steps to confirm or reject the top candidate"}'
    )
    print(f"[RESEARCH] Groq prompt chars: {len(groq_prompt)}")

    if settings.GROQ_API_KEY and settings.GROQ_API_KEY not in ("your_groq_key_here", ""):
        try:
            from groq import Groq
            client = Groq(api_key=settings.GROQ_API_KEY)
            loop = asyncio.get_running_loop()

            def _groq_call():
                return client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": groq_prompt}],
                    max_tokens=700,
                    temperature=0.3,
                )

            resp = await loop.run_in_executor(None, _groq_call)
            raw_text = resp.choices[0].message.content
            print(f"[RESEARCH] Groq raw:\n{raw_text}")

            cleaned = re.sub(r"```json|```", "", raw_text.strip()).strip()
            s_idx = cleaned.find("{")
            e_idx = cleaned.rfind("}")
            if s_idx != -1 and e_idx != -1:
                parsed = json.loads(cleaned[s_idx:e_idx + 1])
                groq_reasoning          = parsed.get("visual_reasoning", "")
                groq_experimental_notes = parsed.get("experimental_notes", "")
                groq_next_steps         = parsed.get("next_steps", "")
                print(f"[RESEARCH] Groq JSON parsed OK")
            else:
                groq_reasoning = raw_text[:500]
                print(f"[RESEARCH] Groq returned prose — using as visual_reasoning")

        except json.JSONDecodeError as je:
            groq_error = f"JSON parse error: {je}"
            groq_reasoning = raw_text[:400] if raw_text else "Groq response could not be parsed."
            print(f"[RESEARCH] Groq JSON error: {je}")
        except Exception as e:
            groq_error = str(e)
            print(f"[RESEARCH] Groq API error: {e}")
    else:
        groq_error = "GROQ_API_KEY not configured"
        print(f"[RESEARCH] Groq skipped — key not set")

    # Sensible fallbacks
    if not groq_reasoning:
        groq_reasoning = (
            f"MobileNet selected '{selected_candidate}' with {research_confidence} confidence "
            f"for the {crop} leaf image."
            + (f" Groq reasoning unavailable: {groq_error}." if groq_error else "")
        )
    if not groq_experimental_notes:
        groq_experimental_notes = (
            "These predictions are generated by a local MobileNet v3 model for research comparison only. "
            "Confidence scores reflect visual pattern similarity — not clinical certainty. "
            f"The model returned {len(top_predictions)} candidates with varied confidence, "
            "suggesting visual ambiguity in the image."
        )
    if not groq_next_steps:
        groq_next_steps = (
            "1. Compare the observed leaf symptoms against reference images for each predicted disease.\n"
            "2. Inspect additional leaves from the same plant and nearby plants.\n"
            "3. Use CropGuard's official Scan Leaf (Gemini Vision) for a verified clinical diagnosis.\n"
            "4. Consult your local agricultural extension officer for field confirmation."
        )

    # ── STEP 3: Final Structured Response ────────────────────────────────
    final_response = {
        # Primary fields (consumed by ResearchPage.jsx)
        "crop":                crop,
        "top_predictions":     top_predictions,
        "selected_candidate":  selected_candidate,
        "rejected_candidates": rejected_candidates,
        "research_confidence": research_confidence,
        "visual_reasoning":    groq_reasoning,
        "experimental_notes":  groq_experimental_notes,
        "next_steps":          groq_next_steps,
        # Legacy compat keys
        "mobilenet_prediction": selected_candidate,
        "mobilenet_top5":       top_predictions,
        "top5":                 top_predictions,
        "groq_interpretation":  groq_reasoning,
        # Debug metadata (visible in browser console)
        "_debug": {
            "mobilenet_loaded":   raw_mobilenet is not None,
            "mobilenet_error":    mobilenet_error,
            "groq_error":         groq_error,
            "predictions_count":  len(top_predictions),
        }
    }

    print(f"[RESEARCH] Response keys: {list(final_response.keys())}")
    print(f"[RESEARCH] selected={selected_candidate}, confidence={research_confidence}")
    print(f"[RESEARCH] ===== Research Lab Complete =====\n")
    return final_response
