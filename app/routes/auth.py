from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.services.auth_service import sign_up, sign_in

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    user_type: str
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def register(data: SignUpRequest):

    try:
        res = sign_up(
            data.email,
            data.password,
            data.full_name,
            data.user_type,
            data.phone
        )

        return {
            "access_token": res.session.access_token,
            "token_type": "bearer",
            "user_id": res.user.id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(data: LoginRequest):

    try:
        res = sign_in(
            data.email,
            data.password
        )

        return {
            "access_token": res.session.access_token,
            "token_type": "bearer",
            "user_id": res.user.id
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            audience="authenticated"
        )

        user_id = payload["sub"]

        return {
            "id": user_id,
            "email": payload.get("email")
        }

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )