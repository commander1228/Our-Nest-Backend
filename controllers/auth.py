from supabase import create_client
from fastapi import HTTPException
from models.models import User
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
import os

load_dotenv()

supabase = create_client(os.getenv("SUPA_URL"), os.getenv("SUPA_KEY"))


class Credentials(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


async def registerUser(email: EmailStr, password: str):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})

        if response.user:
            user = await User.create(id=response.user.id, email=email)

            return AuthResponse(
                access_token=response.session.access_token, 
                refresh_token=response.session.refresh_token,
            )

        raise HTTPException(status_code=400, detail="Registration failed")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
