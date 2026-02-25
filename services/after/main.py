from fastapi import FastAPI, Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import socket
import datetime
import random

app = FastAPI()

SERVICE_NAME = "USER-SERVICE"
VERSION = "v2.0"
STAGE = "AFTER DEPLOYMENT (CANARY)"

REQUEST_COUNT = Counter(
    "after_requests_total",
    "Total requests after deployment"
)

ERROR_COUNT = Counter(
    "after_errors_total",
    "Total errors after deployment"
)


@app.get("/")
async def home(request: Request):

    REQUEST_COUNT.inc()

    hostname = socket.gethostname()
    time = str(datetime.datetime.now())

    print("\n" + "#"*60)
    print("SERVICE:", SERVICE_NAME)
    print("VERSION:", VERSION)
    print("STAGE:", STAGE)
    print("POD:", hostname)
    print("TIME:", time)
    print("#"*60)

    if random.random() < 0.30:
        ERROR_COUNT.inc()

        print("STATUS: ERROR")
        print("!!! NEW VERSION FAILURE !!!")
        print("#"*60)

        return {
            "service": SERVICE_NAME,
            "version": VERSION,
            "stage": STAGE,
            "status": "error",
            "pod": hostname,
            "time": time,
            "visual": "████████ NEW VERSION ████████",
            "warning": "Canary version unstable"
        }

    print("STATUS: SUCCESS")
    print("NEW VERSION RUNNING")
    print("#"*60)

    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "stage": STAGE,
        "status": "success",
        "pod": hostname,
        "time": time,
        "visual": "████████ NEW VERSION ████████"
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
