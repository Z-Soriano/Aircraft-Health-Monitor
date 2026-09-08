from contextlib import asynccontextmanager
from threading import Event, Thread

from fastapi import FastAPI, HTTPException

from groundStation import runGroundStation
from telemetryStore import readLatestTelemetry, updateLatestTelemetry


receiverStopEvent = Event()


@asynccontextmanager
async def lifespan(app: FastAPI):
    receiverStopEvent.clear()

    receiverThread = Thread(
        target=runGroundStation,
        args=(receiverStopEvent, updateLatestTelemetry),
        daemon=True
    )

    receiverThread.start()

    yield

    receiverStopEvent.set()
    receiverThread.join(timeout=2.0)


app = FastAPI(
    title="Aircraft Telemetry API",
    lifespan=lifespan
)


@app.get("/api/telemetry/latest")
def latestTelemetryEndpoint():
    telemetry = readLatestTelemetry()

    if telemetry is None:
        raise HTTPException(
            status_code=503,
            detail="No telemetry has been received yet."
        )

    return telemetry