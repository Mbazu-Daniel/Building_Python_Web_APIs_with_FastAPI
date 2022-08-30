from fastapi import FastAPI, APIRouter
from fastapi_offline import FastAPIOffline
from todo import todo_router

app = FastAPIOffline()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello world"}


app.include_router(todo_router)
