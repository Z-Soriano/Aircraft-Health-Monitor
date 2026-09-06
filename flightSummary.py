import csv


def summarizeFlight(filePath):
    with filePath.open("r", newline="", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        readings = list(reader)

    if not readings:
        print("No telemetry readings were recorded.")
        return

    print("\nFlight Summary")
    print("--------------")
    print(f"Total readings: {len(readings)}")