import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY")
    supabase_jwt_secret: str = os.getenv("SUPABASE_JWT_SECRET")
    supabase_url: str = os.getenv("SUPABASE_URL")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_KEY")
    jwt_secret: str = os.getenv("SUPABASE_JWT_SECRET")

    cloudinary_cloud_name: str = os.getenv("CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = os.getenv("CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = os.getenv("CLOUDINARY_API_SECRET")

    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER")

    sentry_dsn: str = os.getenv("SENTRY_DSN", "")

    fair_price_function_url: str = os.getenv("FAIR_PRICE_FUNCTION_URL")

    class Config:
        env_file = ".env"

settings = Settings()