from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import router
from ticker import ticker


app = FastAPI()


@app.on_event("startup")
def startup_event():
    ticker.run()


@app.on_event("shutdown")
def shutdown_event():
    ticker.stop()


app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
