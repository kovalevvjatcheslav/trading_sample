FROM python:3.10.4-slim AS builder

RUN mkdir /deps

COPY ticker/requirements.txt ./
RUN pip install --target=/deps -r requirements.txt

FROM python:3.10.4-slim

WORKDIR ticker

ENV PYTHONPATH="/deps:/ticker:$PATH"

COPY --from=builder /deps /deps
COPY docker/.env ticker/settings.py ticker/ticker.py ./