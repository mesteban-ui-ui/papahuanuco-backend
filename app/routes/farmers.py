from fastapi import APIRouter, Depends, HTTPException

from app.routes.auth import get_current_user
from app.database import supabase
from app.models.farmer import FarmerProfile, FarmerUpdate

router = APIRouter(
    prefix="/farmers",
    tags=["farmers"]
)


@router.get("/")
async def list_farmers():

    res = supabase.table("profiles") \
        .select("*") \
        .eq("user_type", "productor") \
        .execute()

    return res.data


@router.get("/{farmer_id}")
async def get_farmer(farmer_id: str):

    res = supabase.table("profiles") \
        .select("*") \
        .eq("id", farmer_id) \
        .eq("user_type", "productor") \
        .single() \
        .execute()

    if not res.data:
        raise HTTPException(
            status_code=404,
            detail="Productor no encontrado"
        )

    return res.data


@router.put("/{farmer_id}")
async def update_farmer(
    farmer_id: str,
    data: FarmerUpdate,
    current_user=Depends(get_current_user)
):

    if current_user["id"] != farmer_id:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    res = supabase.table("profiles") \
        .update(data.dict(exclude_unset=True)) \
        .eq("id", farmer_id) \
        .execute()

    return res.data[0]