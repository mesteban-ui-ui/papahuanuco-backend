from fastapi import APIRouter
from app.database import supabase

router = APIRouter(
    tags=["health"]
)

@router.get("/health")
def health():
    return {
        "status": "ok"
    }

@router.get("/metrics")
def metrics():

    # Contar pedidos
    pedidos = supabase.table("orders") \
        .select("id", count="exact") \
        .execute()

    # Contar usuarios
    usuarios = supabase.table("profiles") \
        .select("id", count="exact") \
        .execute()

    return {
        "total_orders": pedidos.count,
        "total_users": usuarios.count
    }