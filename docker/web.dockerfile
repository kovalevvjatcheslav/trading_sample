FROM python:3.10.4-slim AS builder

RUN mkdir /deps

COPY web_service/requirements.txt ./
RUN pip install --target=/deps -r requirements.txt

FROM python:3.10.4-slim

WORKDIR service

ENV PYTHONPATH="/deps:/service:$PATH"

COPY --from=builder /deps /deps
COPY docker/.env web_service/router.py web_service/settings.py web_service/main.py ./
COPY web_service/templates templates
COPY web_service/static static