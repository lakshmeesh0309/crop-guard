from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from typing import Optional
from datetime import datetime, timezone

client: Optional[AsyncIOMotorClient] = None

def get_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGO_URL)
    return client

def get_db():
    return get_client()[settings.MONGO_DB]

# Collections
def users_col():      return get_db()["users"]
def scans_col():      return get_db()["scans"]
def treatments_col(): return get_db()["treatments"]
def notifications_col(): return get_db()["notifications"]

async def init_db():
    db = get_db()
    # Create indexes
    await db["users"].create_index("email", unique=True)
    await db["scans"].create_index("user_id")
    await db["scans"].create_index("created_at")
    await db["treatments"].create_index("slug", unique=True)
    
    # Compound search index for user notifications
    await db["notifications"].create_index([("user_id", 1), ("created_at", -1)])
    await db["notifications"].create_index("read")

    # Seed treatments if empty
    count = await db["treatments"].count_documents({})
    if count == 0:
        await seed_treatments(db)

    # Seed default admin if none exists
    admin_exists = await db["users"].find_one({"role": "admin"})
    if not admin_exists:
        from app.auth import hash_password
        await db["users"].insert_one({
            "name": "CropGuard Admin",
            "email": "admin@cropguard.ai",
            "password_hash": hash_password("Admin@CropGuard2026!"),
            "farm_name": "Admin",
            "location": "Visakhapatnam",
            "crops": [],
            "role": "admin",
            "created_at": datetime.now(timezone.utc),
        })
        print("[OK] Default admin seeded -- CHANGE the password immediately after first login")

    print("[OK] MongoDB connected -- cropguard_db ready")

async def seed_treatments(db):
    treatments = [
        {
            "slug": "rice-blast",
            "disease": "Rice Blast Disease",
            "pathogen": "Magnaporthe oryzae",
            "tag": "Fungicide Required",
            "crops": ["Rice"],
            "steps": [
                {"title": "Primary Fungicide", "description": "Apply Tricyclazole 75 WP at 0.6g/L. Spray at early tillering and heading stages.", "type": "fungicide"},
                {"title": "Water Management", "description": "Drain fields intermittently. Avoid excess nitrogen fertilizer.", "type": "cultural"},
                {"title": "Preventive Spray", "description": "Apply Propiconazole 25 EC at 1ml/L as preventive spray before rain.", "type": "fungicide"},
                {"title": "Field Hygiene", "description": "Remove and burn infected plant residues after harvest.", "type": "cultural"},
            ]
        },
        {
            "slug": "tomato-early-blight",
            "disease": "Tomato Early Blight",
            "pathogen": "Alternaria solani",
            "tag": "Organic Option Available",
            "crops": ["Tomato"],
            "steps": [
                {"title": "Copper Fungicide", "description": "Apply Mancozeb 75 WP at 2g/L every 7 days for 3 weeks.", "type": "fungicide"},
                {"title": "Neem Oil Spray", "description": "Apply 5ml neem oil per litre weekly as organic preventive.", "type": "organic"},
                {"title": "Leaf Removal", "description": "Remove and destroy infected lower leaves immediately.", "type": "cultural"},
                {"title": "Drip Irrigation", "description": "Switch to drip irrigation to keep foliage dry.", "type": "cultural"},
            ]
        },
        {
            "slug": "chilli-leaf-curl",
            "disease": "Chilli Leaf Curl Virus",
            "pathogen": "Begomovirus (whitefly vector)",
            "tag": "Insecticide + Removal",
            "crops": ["Chilli"],
            "steps": [
                {"title": "Vector Control", "description": "Apply Imidacloprid 200 SL at 0.3ml/L to eliminate whitefly vectors.", "type": "insecticide"},
                {"title": "Plant Removal", "description": "Uproot and destroy severely infected plants to prevent spread.", "type": "cultural"},
                {"title": "Reflective Mulch", "description": "Use silver/reflective plastic mulch to deter whiteflies.", "type": "cultural"},
                {"title": "Yellow Sticky Traps", "description": "Install yellow sticky traps at 10 per acre to monitor whiteflies.", "type": "organic"},
            ]
        },
        {
            "slug": "tomato-late-blight",
            "disease": "Tomato Late Blight",
            "pathogen": "Phytophthora infestans",
            "tag": "Systemic Fungicide",
            "crops": ["Tomato"],
            "steps": [
                {"title": "Systemic Fungicide", "description": "Apply Metalaxyl + Mancozeb (Ridomil Gold) at 2.5g/L at first sign.", "type": "fungicide"},
                {"title": "Air Circulation", "description": "Prune lower leaves to improve air circulation.", "type": "cultural"},
                {"title": "Copper Spray", "description": "Apply copper oxychloride 50 WP at 3g/L before rain.", "type": "fungicide"},
                {"title": "Drip Only", "description": "Switch to drip irrigation at soil level only.", "type": "cultural"},
            ]
        },
        {
            "slug": "rice-brown-spot",
            "disease": "Rice Brown Spot",
            "pathogen": "Bipolaris oryzae",
            "tag": "Soil Management",
            "crops": ["Rice"],
            "steps": [
                {"title": "Fungicide", "description": "Apply Edifenphos (Hinosan) 50 EC at 1ml/L at booting stage.", "type": "fungicide"},
                {"title": "Potassium Correction", "description": "Apply 60 kg/ha potassium chloride -- K deficiency increases susceptibility.", "type": "cultural"},
                {"title": "Seed Treatment", "description": "Treat seeds with Thiram 75 WP at 2g/kg before planting.", "type": "fungicide"},
                {"title": "Field Monitoring", "description": "Inspect fields closely after rain events.", "type": "cultural"},
            ]
        },
        {
            "slug": "cotton-bollworm",
            "disease": "Cotton Bollworm",
            "pathogen": "Helicoverpa armigera",
            "tag": "Integrated Pest Management",
            "crops": ["Cotton"],
            "steps": [
                {"title": "Bt Spray", "description": "Apply Bacillus thuringiensis (Bt) at 2g/L -- safe biological control.", "type": "organic"},
                {"title": "Pheromone Traps", "description": "Install pheromone traps at 5 per acre. Replace lures every 3 weeks.", "type": "organic"},
                {"title": "Chemical Control", "description": "If >5 larvae/plant apply Spinosad 45 SC at 0.3ml/L.", "type": "insecticide"},
            ]
        },
        {
            "slug": "general-prevention",
            "disease": "General Prevention",
            "pathogen": "All crops",
            "tag": "Best Practice",
            "crops": ["Rice", "Tomato", "Chilli", "Cotton", "Groundnut", "Maize"],
            "steps": [
                {"title": "Certified Seeds", "description": "Always use certified disease-resistant seed varieties.", "type": "cultural"},
                {"title": "Crop Rotation", "description": "Rotate crops seasonally -- never same crop two seasons in a row.", "type": "cultural"},
                {"title": "Field Hygiene", "description": "Remove and destroy crop residues after harvest.", "type": "cultural"},
                {"title": "Regular Scanning", "description": "Scan leaves with CropGuard AI every 7-10 days for early detection.", "type": "cultural"},
            ]
        },
    ]
    await db["treatments"].insert_many(treatments)
    print("[OK] Treatment data seeded")

async def create_notification(user_id: str, type: str, title: str, message: str, metadata: dict = None):
    from bson import ObjectId
    db = get_db()
    try:
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
    except Exception:
        user = None
    
    if user:
        prefs = user.get("notification_preferences", {})
        pref_map = {
            "Scan Completed": "scan_alerts",
            "High Disease Risk": "disease_alerts",
            "Weather Alerts": "weather_alerts",
            "Treatment Reminders": "treatment_reminders"
        }
        pref_key = pref_map.get(type)
        if pref_key and not prefs.get(pref_key, True):
            # User disabled this type of notification
            return None

    notification = {
        "user_id": user_id,
        "type": type,
        "title": title,
        "message": message,
        "read": False,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc)
    }
    col = db["notifications"]
    await col.insert_one(notification)
    return notification
