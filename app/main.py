import os

from fastapi import FastAPI
from app.auth.auth_router import router as auth_router
from app.routers.user_router import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    # ONLY WHILE DEVELOPING
    os.system("uvicorn main:app --reload")
