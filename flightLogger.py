import csv

from datetime import datetime, timezone
from pathlib import Path


fieldNames = [
    "sequenceNumber",
    "timestamp",
    "altitudeFt",
    "speedMph",
    "batteryPercent",
    "temperatureC",
    "status",
    "warnings"
]


def createFlightLog():
    projectDirectory = Path(__file__).resolve().parent
    dataDirectory = projectDirectory / "data"

    dataDirectory.mkdir(parents=True, exist_ok=True)

    flightStart = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    filePath = dataDirectory / f"flight_{flightStart}.csv"

    with filePath.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

    return filePath

def saveReading(filePath, telemetry, healthWarnings):
    status = "WARNING" if healthWarnings else "NORMAL"
    warningText = "; ".join(healthWarnings)

    row = {
        "sequenceNumber": telemetry["sequenceNumber"],
        "timestamp": telemetry["timestamp"],
        "altitudeFt": round(telemetry["altitude"], 2),
        "speedMph": round(telemetry["speed"], 2),
        "batteryPercent": round(telemetry["battery"], 2),
        "temperatureC": round(telemetry["temp"], 2),
        "status": status,
        "warnings": warningText
    }

    with filePath.open("a", newline="", encoding="utf-8") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writerow(row)