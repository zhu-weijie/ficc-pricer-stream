# market_data_publisher/Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install redis

CMD ["python", "-u", "publisher.py"]
