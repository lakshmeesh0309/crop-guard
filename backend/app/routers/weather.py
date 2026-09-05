from fastapi import APIRouter, Query
from app.config import settings
import httpx

router = APIRouter(prefix="/weather", tags=["Weather"])


def disease_risk(h, t, rain):
    score = 0
    if h > 85: score += 3
    elif h > 75: score += 2
    elif h > 65: score += 1
    if 20 <= t <= 32: score += 2
    elif 15 <= t <= 35: score += 1
    if rain > 10: score += 2
    elif rain > 3: score += 1
    return "High" if score >= 6 else "Medium" if score >= 3 else "Low"


@router.get("/current")
async def current(
    lat: float = Query(None),
    lon: float = Query(None),
):
    lat = lat or settings.DEFAULT_LAT
    lon = lon or settings.DEFAULT_LON
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"lat": lat, "lon": lon, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"}
            )
            if r.status_code == 200:
                d    = r.json()
                h    = d["main"]["humidity"]
                t    = d["main"]["temp"]
                rain = d.get("rain", {}).get("1h", 0)
                return {
                    "location":    settings.DEFAULT_CITY,
                    "temp":        round(t, 1),
                    "feels_like":  round(d["main"]["feels_like"], 1),
                    "humidity":    h,
                    "wind_speed":  round(d["wind"]["speed"] * 3.6, 1),
                    "description": d["weather"][0]["description"].title(),
                    "rain_1h":     rain,
                    "disease_risk": disease_risk(h, t, rain),
                }
    except Exception:
        pass
    return _mock_current()


@router.get("/forecast")
async def forecast(lat: float = Query(None), lon: float = Query(None)):
    lat = lat or settings.DEFAULT_LAT
    lon = lon or settings.DEFAULT_LON
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={"lat": lat, "lon": lon, "appid": settings.OPENWEATHER_API_KEY, "units": "metric", "cnt": 40}
            )
            if r.status_code == 200:
                from datetime import datetime
                data = r.json()
                days_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                days, results = {}, []
                for item in data["list"]:
                    day = item["dt_txt"][:10]
                    if day not in days:
                        days[day] = item
                        h    = item["main"]["humidity"]
                        t    = item["main"]["temp"]
                        rain = item.get("rain", {}).get("3h", 0)
                        dt   = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                        results.append({
                            "day":          days_names[dt.weekday()],
                            "temp_max":     round(t, 1),
                            "temp_min":     round(item["main"]["temp_min"], 1),
                            "humidity":     h,
                            "rain":         round(rain, 1),
                            "disease_risk": disease_risk(h, t, rain),
                        })
                return results[:7]
    except Exception:
        pass
    return _mock_forecast()


@router.get("/advisory")
async def advisory(lat: float = Query(None), lon: float = Query(None)):
    cur  = await current(lat=lat, lon=lon)
    hum  = cur.get("humidity", 70)
    temp = cur.get("temp", 28)
    risk = cur.get("disease_risk", "Low")
    advisories = []
    if hum > 80:
        advisories += [
            {"crop":"Rice",  "alert":"High Risk","message":f"Humidity {hum}% — prime for Rice Blast. Apply Tricyclazole immediately."},
            {"crop":"Tomato","alert":"High Risk","message":"High humidity favors Blight. Apply Mancozeb before next rain."},
            {"crop":"Wheat", "alert":"High Risk","message":"Coastal humidity favors stripe rust. Apply Propiconazole at flag leaf."},
        ]
    if hum > 70:
        advisories += [
            {"crop":"Chilli",    "alert":"Medium Risk","message":"Whitefly activity up. Monitor for Leaf Curl Virus spread."},
            {"crop":"Groundnut", "alert":"Medium Risk","message":"Humid conditions promote leaf spot. Apply Mancozeb preventively."},
            {"crop":"Sugarcane", "alert":"Medium Risk","message":"Wet conditions increase red rot risk. Inspect stalks at soil level."},
        ]
    advisories += [
        {"crop":"Cotton","alert":"Low Risk" if hum < 75 else "Medium Risk","message":"Monitor bollworm pheromone traps weekly."},
        {"crop":"Maize", "alert":"Low Risk" if hum < 80 else "Medium Risk","message":"Check lower leaves for northern leaf blight."},
    ]
    return {"overall_risk":risk,"summary":f"{'High humidity' if hum>80 else 'Moderate'} at {temp}°C in Visakhapatnam. {risk} disease risk today.","advisories":advisories}


def _mock_current():
    return {"location":"Visakhapatnam","temp":31.0,"feels_like":34.0,"humidity":82,"wind_speed":14.0,"description":"Coastal Breeze","rain_1h":0.0,"disease_risk":"Medium"}

def _mock_forecast():
    return [
        {"day":"Today",    "temp_max":31,"temp_min":25,"humidity":82,"rain":0, "disease_risk":"Medium"},
        {"day":"Tomorrow", "temp_max":29,"temp_min":24,"humidity":88,"rain":5, "disease_risk":"High"},
        {"day":"Wednesday","temp_max":28,"temp_min":23,"humidity":90,"rain":12,"disease_risk":"High"},
        {"day":"Thursday", "temp_max":30,"temp_min":24,"humidity":85,"rain":2, "disease_risk":"Medium"},
        {"day":"Friday",   "temp_max":32,"temp_min":26,"humidity":75,"rain":0, "disease_risk":"Low"},
        {"day":"Saturday", "temp_max":33,"temp_min":27,"humidity":70,"rain":0, "disease_risk":"Low"},
        {"day":"Sunday",   "temp_max":31,"temp_min":25,"humidity":78,"rain":3, "disease_risk":"Medium"},
    ]
