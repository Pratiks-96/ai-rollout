from fastapi import FastAPI, Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import socket
import datetime
import random

app = FastAPI()

SERVICE_NAME = "USER-SERVICE"
VERSION = "v1.0"
STAGE = "BEFORE DEPLOYMENT (STABLE)"

REQUEST_COUNT = Counter(
    "before_requests_total",
    "Total requests before deployment"
)

ERROR_COUNT = Counter(
    "before_errors_total",
    "Total errors before deployment"
)


@app.get("/")
async def home(request: Request):

    REQUEST_COUNT.inc()

    hostname = socket.gethostname()
    time = str(datetime.datetime.now())

    print("\n" + "="*60)
    print("SERVICE:", SERVICE_NAME)
    print("VERSION:", VERSION)
    print("STAGE:", STAGE)
    print("POD:", hostname)
    print("TIME:", time)
    print("="*60)

    if random.random() < 0.05:
        ERROR_COUNT.inc()

        print("STATUS: ERROR")
        print("="*60)

        return {
            "service": SERVICE_NAME,
            "version": VERSION,
            "stage": STAGE,
            "status": "error",
            "pod": hostname,
            "time": time,
            "visual": "████████ STABLE VERSION ████████"
        }

    print("STATUS: SUCCESS")
    print("="*60)

    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "stage": STAGE,
        "status": "success",
        "pod": hostname,
        "time": time,
        "visual": "████████ STABLE VERSION ████████"
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
