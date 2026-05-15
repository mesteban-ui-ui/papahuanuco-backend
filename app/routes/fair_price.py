from fastapi import APIRouter, HTTPException
import httpx

from app.config import settings


router = APIRouter(
    prefix="/fair-price",
    tags=["fair-price"]
)


@router.post("/")
async def get_fair_price(
    variety: str,
    quantity_kg: int,
    altitude: int
):

    # Si NO existe una IA real todavía
    if not settings.fair_price_function_url:

        precios_simulados = {

            "Papa Amarilla": 3.80,

            "Papa Huayro": 3.20,

            "Papa Yungay": 2.80,

            "Papa Peruanita": 3.50,

            "Papas Nativas": 4.50
        }

        base = precios_simulados.get(variety, 3.00)

        return {
            "suggested_price": base
        }

    # Si ya existe IA real
    async with httpx.AsyncClient() as client:

        response = await client.post(
            settings.fair_price_function_url,
            json={
                "variety": variety,
                "quantity_kg": quantity_kg,
                "altitude": altitude
            }
        )

        if response.status_code == 200:
            return response.json()

        raise HTTPException(
            status_code=500,
            detail="Error al obtener precio justo"
        )