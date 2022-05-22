from asyncio import sleep, exceptions

from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from redis.asyncio import Redis
from websockets.exceptions import ConnectionClosedOK

from controller import DataController
from settings import settings
from templates.template_processor import template_processor


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # TODO: have to add tickers list to template
    return template_processor.TemplateResponse("index.html", {"request": request})


@router.get("/ticker_entries/{ticker_name}")
async def get_entries(ticker_name: str):
    return await DataController.get_all_ticker_entries(ticker_name)


@router.websocket("/realtime_data")
async def get_realtime(websocket: WebSocket):
    await websocket.accept()
    # TODO: move retrieve data from redis into controller
    redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    channel = redis_client.pubsub()
    await channel.subscribe("ticker_1")
    while True:
        try:
            msg = await channel.get_message(ignore_subscribe_messages=True)
            if msg is not None:
                await websocket.send_json({"ticker_1": msg["data"].decode("utf8")})
            await sleep(0.1)
        except (ConnectionClosedOK, exceptions.CancelledError):
            return
