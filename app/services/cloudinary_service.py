import cloudinary
import cloudinary.uploader

from fastapi import UploadFile

from app.config import settings


cloudinary.config(

    cloud_name=settings.cloudinary_cloud_name,

    api_key=settings.cloudinary_api_key,

    api_secret=settings.cloudinary_api_secret

)

async def upload_image(file: UploadFile) -> str:

    contents = await file.read()

    result = cloudinary.uploader.upload(
        contents,
        folder="papahuanuco"
    )

    return result["secure_url"]