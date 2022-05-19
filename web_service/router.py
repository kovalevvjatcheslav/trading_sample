import json

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
    print(await DataController.get_all_ticker_entries("ticker_1"))
    return template_processor.TemplateResponse("index.html", {"request": request})


@router.websocket("/realtime_data")
async def get_realtime(websocket: WebSocket):
    await websocket.accept()
    redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    while True:
        subscription = redis_client.pubsub()
        await subscription.subscribe("ticker_1")
        async for msg in subscription.listen():
            if msg.get("type") == "message":
                try:
                    await websocket.send_json(json.dumps({"key": msg["data"].decode("utf8")}))
                except ConnectionClosedOK:
                    return
