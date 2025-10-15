
FROM python:3.14.0-slim

WORKDIR /aggregator

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN --mount=type=cache,sharing=locked,target=/root/.cache/pip \
    pip install --disable-pip-version-check -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80", "--workers", "4"]
