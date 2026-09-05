from fastapi import APIRouter, HTTPException, Query
from app.database import treatments_col

router = APIRouter(prefix="/treatments", tags=["Treatments"])


def serialize(t):
    t["id"] = str(t.pop("_id"))
    return t


@router.get("/")
async def list_treatments(crop: str = Query(None), search: str = Query(None)):
    col     = treatments_col()
    query   = {}
    if crop:   query["crops"] = crop
    if search: query["$or"] = [{"disease": {"$regex": search, "$options":"i"}}, {"pathogen": {"$regex": search, "$options":"i"}}]
    items = await col.find(query).to_list(length=100)
    return [serialize(t) for t in items]


@router.get("/disease/{disease_name}")   # MUST be before /{slug}
async def get_by_disease(disease_name: str):
    col   = treatments_col()
    t     = await col.find_one({"disease": {"$regex": disease_name, "$options": "i"}})
    if not t:
        t = await col.find_one({"slug": "general-prevention"})
    return serialize(t) if t else {"message": "No treatment found"}


@router.get("/{slug}")
async def get_treatment(slug: str):
    col = treatments_col()
    t   = await col.find_one({"slug": slug})
    if not t:
        raise HTTPException(404, "Treatment not found")
    return serialize(t)
