FROM python:3.10

WORKDIR /app

COPY main.py .

RUN pip install fastapi uvicorn prometheus_client

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
