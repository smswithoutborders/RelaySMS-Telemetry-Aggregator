
FROM python:3.14.3-slim

WORKDIR /aggregator

COPY requirements.txt .

RUN --mount=type=cache,sharing=locked,target=/root/.cache/pip \
    pip install --disable-pip-version-check -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80", "--workers", "4"]
