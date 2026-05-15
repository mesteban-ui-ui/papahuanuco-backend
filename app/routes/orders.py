from fastapi import APIRouter, Depends, HTTPException

from app.routes.auth import get_current_user
from app.database import supabase

from app.models.order import (
    OrderCreate,
    OrderStatusUpdate
)

from app.services.twilio_service import send_sms_to_farmer


router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.post("/")
async def create_order(
    data: OrderCreate,
    current_user=Depends(get_current_user)
):

    buyer_id = current_user["id"]

    # Buscar cosecha
    harvest = supabase.table("harvests") \
        .select("*") \
        .eq("id", data.harvest_id) \
        .single() \
        .execute()

    # Verificar disponibilidad
    if not harvest.data or not harvest.data["available"]:

        raise HTTPException(
            status_code=400,
            detail="Cosecha no disponible"
        )

    # Verificar stock
    if harvest.data["quantity_kg"] < data.quantity_kg:

        raise HTTPException(
            status_code=400,
            detail="Stock insuficiente"
        )

    # Precio total
    total_price = (
        data.quantity_kg *
        harvest.data["price_per_kg"]
    )

    # Crear pedido
    order = {

        "harvest_id": data.harvest_id,

        "buyer_id": buyer_id,

        "quantity_kg": data.quantity_kg,

        "total_price": total_price,

        "payment_method": data.payment_method,

        "status": "pendiente"
    }

    res = supabase.table("orders") \
        .insert(order) \
        .execute()

    # Actualizar stock
    new_quantity = (
        harvest.data["quantity_kg"] -
        data.quantity_kg
    )

    supabase.table("harvests") \
        .update({
            "quantity_kg": new_quantity,
            "available": new_quantity > 0
        }) \
        .eq("id", data.harvest_id) \
        .execute()

    # Buscar productor
    farmer = supabase.table("profiles") \
        .select("phone, full_name") \
        .eq("id", harvest.data["farmer_id"]) \
        .single() \
        .execute()

    # Enviar SMS
    if farmer.data and farmer.data["phone"]:

        await send_sms_to_farmer(
            farmer.data["phone"],
            farmer.data["full_name"],
            data.quantity_kg,
            harvest.data["variety"]
        )

    return res.data[0]


@router.get("/")
async def list_orders(
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    profile = supabase.table("profiles") \
        .select("user_type") \
        .eq("id", user_id) \
        .single() \
        .execute()

    if not profile.data:

        raise HTTPException(
            status_code=404,
            detail="Perfil no encontrado"
        )

    # PRODUCTOR
    if profile.data["user_type"] == "productor":

        harvests = supabase.table("harvests") \
            .select("id") \
            .eq("farmer_id", user_id) \
            .execute()

        if harvests.data:

            ids = [h["id"] for h in harvests.data]

            res = supabase.table("orders") \
                .select("*, harvest:harvests(variety)") \
                .in_("harvest_id", ids) \
                .execute()

        else:

            return []

    # COMPRADOR
    else:

        res = supabase.table("orders") \
            .select(
                "*, harvest:harvests(variety, farmer:profiles(full_name))"
            ) \
            .eq("buyer_id", user_id) \
            .execute()

    return res.data


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    current_user=Depends(get_current_user)
):

    order = supabase.table("orders") \
        .select("harvest_id") \
        .eq("id", order_id) \
        .single() \
        .execute()

    if not order.data:

        raise HTTPException(status_code=404)

    harvest = supabase.table("harvests") \
        .select("farmer_id") \
        .eq("id", order.data["harvest_id"]) \
        .single() \
        .execute()

    # Verificar dueño
    if not harvest.data or \
       harvest.data["farmer_id"] != current_user["id"]:

        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    supabase.table("orders") \
        .update({
            "status": data.status
        }) \
        .eq("id", order_id) \
        .execute()

    return {
        "message": "Estado actualizado"
    }