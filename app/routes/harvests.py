import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from app.routes.auth import get_current_user
from app.database import supabase
from app.models.harvest import HarvestCreate, HarvestUpdate
from app.services.cloudinary_service import upload_image

router = APIRouter(
    prefix="/harvests",
    tags=["harvests"]
)


@router.post("/")
async def create_harvest(

    data: HarvestCreate = Depends(),
    image: UploadFile = File(None),
    current_user=Depends(get_current_user)

):

    farmer_id = current_user["id"]

    photo_url = None

    if image:
        photo_url = await upload_image(image)

    trace_code = f"PH-{uuid.uuid4().hex[:8].upper()}"

    record = {

        "farmer_id": farmer_id,
        "variety": data.variety,
        "quantity_kg": data.quantity_kg,
        "price_per_kg": data.price_per_kg,

        "harvest_date": str(data.harvest_date)
        if data.harvest_date else None,

        "method": data.method,
        "fertilization": data.fertilization,

        "ciclo_dias": data.ciclo_dias,
        "altitude": data.altitude,

        "latitude": data.latitude,
        "longitude": data.longitude,

        "photo_url": photo_url,

        "traceability_code": trace_code
    }

    res = supabase.table("harvests") \
        .insert(record) \
        .execute()

    return res.data[0]


@router.get("/")
async def list_harvests(

    variety: str = None,
    available: bool = True

):

    query = supabase.table("harvests") \
        .select("*") \
        .eq("available", available)

    if variety:
        query = query.eq("variety", variety)

    res = query.execute()

    return res.data


@router.get("/{harvest_id}")
async def get_harvest(harvest_id: str):

    res = supabase.table("harvests") \
        .select(
            "*, farmer:profiles(full_name, location, certifications, photo_url)"
        ) \
        .eq("id", harvest_id) \
        .single() \
        .execute()

    if not res.data:

        raise HTTPException(
            status_code=404,
            detail="Cosecha no encontrada"
        )

    return res.data


@router.put("/{harvest_id}")
async def update_harvest(

    harvest_id: str,
    data: HarvestUpdate,
    current_user=Depends(get_current_user)

):

    harvest = supabase.table("harvests") \
        .select("farmer_id") \
        .eq("id", harvest_id) \
        .single() \
        .execute()

    if not harvest.data:

        raise HTTPException(
            status_code=404,
            detail="Cosecha no encontrada"
        )

    if harvest.data["farmer_id"] != current_user["id"]:

        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    supabase.table("harvests") \
        .update(data.dict(exclude_unset=True)) \
        .eq("id", harvest_id) \
        .execute()

    return {
        "message": "Actualizado"
    }