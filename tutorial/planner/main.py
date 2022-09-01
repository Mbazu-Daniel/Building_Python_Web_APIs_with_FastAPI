from fastapi import FastAPI
from fastapi_offline import FastAPIOffline
from database.connection import conn

from routes.users import user_router
from routes.events import event_router

import uvicorn

app = FastAPIOffline()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.on_event("startup")
def on_startup():
    conn()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
