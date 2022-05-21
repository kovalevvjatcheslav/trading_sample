from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from router import router
from settings import settings
from sources import db


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await db.create_pool()
    await db.create_table()


@app.on_event("shutdown")
async def shutdown_event():
    await db.close_pool()


app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.WEB_SERVICE_PORT, log_level="info")
