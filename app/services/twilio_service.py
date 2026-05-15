from twilio.rest import Client

from app.config import settings


client = Client(
    settings.twilio_account_sid,
    settings.twilio_auth_token
)


async def send_sms_to_farmer(
    phone: str,
    farmer_name: str,
    quantity: int,
    variety: str
):

    # Si no hay número Twilio configurado
    if not settings.twilio_phone_number:
        print("Twilio no configurado todavía")
        return "mock_sms"

    message = client.messages.create(

        body=f"Hola {farmer_name}, tienes un nuevo pedido de {quantity} kg de {variety}. Revisa la app para confirmar.",

        from_=settings.twilio_phone_number,

        to=phone
    )

    return message.sid