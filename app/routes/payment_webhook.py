from fastapi import APIRouter, Request

from app.database import supabase


router = APIRouter(
    prefix="/webhooks/payment",
    tags=["payment"]
)


@router.post("/")
async def payment_webhook(request: Request):

    body = await request.json()

    # JSON simulado
    # {
    #   "order_id": "uuid",
    #   "status": "success",
    #   "payment_id": "sim_1234"
    # }

    order_id = body.get("order_id")

    # Verificar order_id
    if not order_id:

        return {
            "error": "order_id requerido"
        }

    # Actualizar pago
    supabase.table("orders") \
        .update({
            "payment_status": "completado"
        }) \
        .eq("id", order_id) \
        .execute()

    return {
        "message": "Pago registrado (mock)"
    }