from fastapi import FastAPI, APIRouter, Depends
from controllers import auth
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

register_tortoise(
    app,
    db_url=os.getenv("DB_URL"),
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

protected = APIRouter(dependencies=[Depends(auth.get_current_user)])


@app.get("/")
def root():
    return {"message": "wassup"}


@app.post("/auth/register", response_model=auth.AuthResponse)
async def registerUser(request: auth.Credentials):
    return await auth.registerUser(request.model_dump())


@app.post("/auth/login", response_model=auth.AuthResponse)
async def loginUser(request: auth.Credentials):
    return await auth.loginUser(request.model_dump())


@app.post("/auth/refresh", response_model=auth.AuthResponse)
async def refresh(request: auth.RefreshRequest):
    return await auth.refresh_token(request.refresh_token)
