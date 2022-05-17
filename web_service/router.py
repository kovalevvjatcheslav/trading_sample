import json

from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from redis.asyncio import Redis
from websockets.exceptions import ConnectionClosedOK

from templates.template_processor import template_processor


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return template_processor.TemplateResponse("index.html", {"request": request})


@router.websocket("/realtime_data")
async def get_realtime(websocket: WebSocket):
    await websocket.accept()
    redis_client = Redis(host='localhost', port=6379, db=0)
    while True:
        subscription = redis_client.pubsub()
        await subscription.subscribe("ticker_1")
        async for msg in subscription.listen():
            try:
                await websocket.send_json(json.dumps({"key": msg}))
            except ConnectionClosedOK:
                return
