# CropGuard AI v3 — MongoDB Edition
# Visakhapatnam · Weather API Integrated · Premium UI

## What's New in v3
- ✅ MongoDB instead of MySQL (no SQL Workbench needed)
- ✅ Beautiful premium UI (green/dark theme)
- ✅ Working login & register pages
- ✅ Live Visakhapatnam weather via OpenWeatherMap
- ✅ All pages connected to real database
- ✅ JWT authentication (no Firebase needed)

---

## Install These First (one time)

### 1. Python 3.11+
- Download: https://python.org/downloads
- ⚠️ TICK "Add Python to PATH" during install

### 2. Node.js 20+
- Download: https://nodejs.org (LTS version)

### 3. MongoDB Community Server
- Download: https://www.mongodb.com/try/download/community
- Choose: Windows · Version 7.0 · MSI package
- ⚠️ During install, CHECK "Install MongoD as a Service"
- This runs MongoDB automatically in background

---

## Running the App

### First time only:
Double-click `setup.bat` — installs all packages

### Every time:
Double-click `START-APP.bat` — starts everything + opens browser

**App:** http://localhost:5173
**API Docs:** http://localhost:8000/docs

---

## What's Hardcoded
- Weather API Key: OpenWeatherMap (your key)
- City: Visakhapatnam (lat: 17.6868, lon: 83.2185)
- MongoDB: localhost:27017 (local, no password needed)
- JWT Secret: auto-configured

---

## MongoDB Notes
- Database name: `cropguard_db`
- Collections: `users`, `scans`, `treatments`
- View data: Install MongoDB Compass (free GUI)
  → https://www.mongodb.com/products/compass
  → Connect to: mongodb://localhost:27017

---

## Features
| Feature | Status |
|---------|--------|
| Register / Login | ✅ Real JWT auth |
| Leaf upload + AI scan | ✅ Saved to MongoDB |
| Detection history | ✅ Real MongoDB data |
| Delete scans | ✅ Removes from DB + file |
| Treatment guide | ✅ From MongoDB |
| Profile save | ✅ Updates MongoDB |
| Dashboard stats | ✅ Calculated from real scans |
| Weather (Vizag) | ✅ Live OpenWeatherMap API |

---

## Deploying Later
MongoDB → MongoDB Atlas (free 512MB cloud cluster)
Backend  → Railway.app (free tier)
Frontend → Netlify or Vercel (free)
Just change MONGO_URL in backend/.env to your Atlas URL.
