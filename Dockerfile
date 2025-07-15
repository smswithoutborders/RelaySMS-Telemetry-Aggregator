
FROM python:3.13.5-slim

WORKDIR /aggregator

COPY requirements.txt .

RUN --mount=type=cache,sharing=locked,target=/root/.cache/pip \
    pip install --disable-pip-version-check --quiet --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80", "--workers", "4"]
