from fastapi import APIRouter, Request


router = APIRouter(
    tags=["sms"]
)


@router.post("/sms/status")
async def sms_status(request: Request):

    data = await request.form()

    print("SMS Status:", data)

    return {
        "ok": True
    }