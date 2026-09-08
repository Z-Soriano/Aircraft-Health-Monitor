from threading import Lock


latestTelemetry = None
telemetryLock = Lock()


def updateLatestTelemetry(telemetry):
    global latestTelemetry

    with telemetryLock:
        latestTelemetry = telemetry.copy()


def readLatestTelemetry():
    with telemetryLock:
        if latestTelemetry is None:
            return None

        return latestTelemetry.copy()