FROM python:3.10.4-slim AS builder

COPY requirements.txt ./
RUN pip install -r requirements.txt

FROM builder

WORKDIR service
COPY router.py main.py ./
COPY templates templates
COPY static static

ENTRYPOINT ["uvicorn","--host=0.0.0.0", "main:app"]