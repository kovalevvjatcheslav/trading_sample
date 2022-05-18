from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from router import router


app = FastAPI()


app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
