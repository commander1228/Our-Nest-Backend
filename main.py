from fastapi import FastAPI, HTTPException
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


@app.get("/")
def root():
    return {"message": "wassup"}


@app.post("/register", response_model=auth.AuthResponse)
async def registerUser(request: auth.Credentials):
    return await auth.registerUser(request.email, request.password)