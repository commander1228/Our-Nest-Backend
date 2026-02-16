from supabase import create_client
from fastapi import HTTPException, Request, Depends
from models.models import User
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

load_dotenv()

supabase = create_client(os.getenv("SUPA_URL"), os.getenv("SUPA_KEY"))
security = HTTPBearer()


class Credentials(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


async def registerUser(request_data: dict):
    try:
        response = supabase.auth.sign_up(request_data)

        if response.user:
            await User.create(id=response.user.id, email=response.user.email)

            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
            )

        raise HTTPException(status_code=400, detail="Registration failed")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def loginUser(request_data: dict):
    try:
        response = supabase.auth.sign_in_with_password(request_data)

        if response.user:
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
            )

        raise HTTPException(status_code=401, detail="Invalid credentials")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        token = credentials.credentials

        user = supabase.auth.get_user(token)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user.user

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def refresh_token(refresh_token: str):
    try:
        response = supabase.auth.refresh_session(refresh_token)

        if response.session:
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
            )

        raise HTTPException(status_code=401, detail="Invalid refresh token")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Could not refresh session")
