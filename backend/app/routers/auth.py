from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime, timezone
from app.database import users_col
from app.auth import hash_password, verify_password, create_token, serialize_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    name:     str
    email:    EmailStr
    password: str
    farmName: str = ""
    location: str = ""
    crops:    List[str] = []


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


@router.post("/register")
async def register(body: RegisterRequest):
    col = users_col()
    if await col.find_one({"email": body.email.lower()}):
        raise HTTPException(400, "Email already registered. Please login.")

    user = {
        "name":          body.name,
        "email":         body.email.lower(),
        "password_hash": hash_password(body.password),
        "farm_name":     body.farmName,
        "location":      body.location,
        "crops":         body.crops,
        "role":          "farmer",
        "notification_preferences": {
            "weather_alerts": True,
            "disease_alerts": True,
            "scan_alerts": True,
            "treatment_reminders": True
        },
        "created_at":    datetime.now(timezone.utc),
    }
    result = await col.insert_one(user)
    user["_id"] = result.inserted_id
    token = create_token(str(result.inserted_id))
    return {"access_token": token, "token_type": "bearer", "user": serialize_user(user)}


@router.post("/login")
async def login(body: LoginRequest):
    col  = users_col()
    user = await col.find_one({"email": body.email.lower()})
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(401, "Incorrect email or password")
    token = create_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer", "user": serialize_user(user)}


@router.get("/me")
async def me(user=Depends(get_current_user)):
    return serialize_user(user)
