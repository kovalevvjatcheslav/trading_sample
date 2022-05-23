from asyncio import sleep, exceptions
import json

from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from redis.asyncio import Redis
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from controller import DataController
from settings import settings
from templates.template_processor import template_processor


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    ticker_names = await DataController.get_ticker_names()
    return template_processor.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ticker_names": sorted(ticker_names, key=lambda item: int(item.split("_")[1])),
        },
    )


@router.get("/ticker_entries/{ticker_name}")
async def get_entries(ticker_name: str):
    return await DataController.get_all_ticker_entries(ticker_name)


@router.websocket("/realtime_data/{ticker_name}")
async def get_realtime(ticker_name: str, websocket: WebSocket):
    await websocket.accept()
    redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    channel = redis_client.pubsub()
    await channel.subscribe(ticker_name)
    while True:
        try:
            msg = await channel.get_message(ignore_subscribe_messages=True)
            if msg is not None:
                await websocket.send_json(json.loads(msg["data"]))
            await sleep(0.01)
        except (ConnectionClosedOK, ConnectionClosedError):
            return
        except exceptions.CancelledError:
            await websocket.close()
            return
