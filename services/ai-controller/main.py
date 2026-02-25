from fastapi import FastAPI
import requests

app = FastAPI()

PROMETHEUS = "http://13.233.162.2:9090"


def get_error_rate(metric):
    query = f'rate({metric}[1m])'
    r = requests.get(
        f"{PROMETHEUS}/api/v1/query",
        params={"query": query}
    )
    data = r.json()

    if len(data["data"]["result"]) == 0:
        return 0

    return float(data["data"]["result"][0]["value"][1])


@app.get("/decision")
def decision():

    before_error = get_error_rate("before_errors_total")
    after_error = get_error_rate("after_errors_total")

    print("before:", before_error)
    print("after:", after_error)

    if after_error > before_error:
        return {
            "decision": "rollback"
        }

    return {
        "decision": "rollout"
    }
