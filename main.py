from ticker import ticker
from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
def startup_event():
    ticker.run()


@app.on_event("shutdown")
def shutdown_event():
    ticker.stop()


@app.get("/")
async def root():
    return {"message": list(ticker.tickers_array)}
