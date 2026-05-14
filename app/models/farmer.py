from pydantic import BaseModel


class FarmerProfile(BaseModel):

    full_name: str
    phone: str | None = None
    location: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    altitude: int | None = None
    experience_years: int | None = None

    certifications: list[str] | None = []


class FarmerUpdate(FarmerProfile):
    pass