
FROM python:3.13.1-slim

WORKDIR /aggregator

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80", "--workers", "4"]
