import json

from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from websockets.exceptions import ConnectionClosedOK

from templates.template_processor import template_processor
from ticker import ticker


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return template_processor.TemplateResponse("index.html", {"request": request})


@router.websocket("/realtime_data")
async def get_realtime(websocket: WebSocket):
    await websocket.accept()
    from time import time
    from asyncio import sleep
    while True:
        try:
            t = time()
            await websocket.send_json(json.dumps({"key": t}))
            print(t)
            await sleep(5)
        except ConnectionClosedOK:
            pass
