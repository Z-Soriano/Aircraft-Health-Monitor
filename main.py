import time

from telemetryGenerator import generateTelemetry
from healthMonitor import checkHealth
from flightLogger import createFlightLog, saveReading
from flightSummary import summarizeFlight
# telemetry = {
#     "altitude": 5000.0, 
#     "speed": 120.0,
#     "battery": 100.0,
#     "temp": 75.0
# }
telemetry = {
    "altitude": 500,
    "speed": 40,
    "battery": 10,
    "temp": 110
}
logFile = createFlightLog()
print(f"Saving flight data to: {logFile}")
try:
    while True:
        telemetry = generateTelemetry(telemetry)
        warnings = checkHealth(telemetry)
        saveReading(logFile, telemetry, warnings)
        print(
            f"Time: {telemetry['timestamp']} | "
            f"Altitude: {telemetry['altitude']:.1f} ft | "
            f"Speed: {telemetry['speed']:.1f} mph | "
            f"Battery: {telemetry['battery']:.1f}% | "
            f"Temperature: {telemetry['temp']:.1f}°C"
        )

        if warnings:
            print("WARNING:", ", ".join(warnings))
        else:
            print("Status: NORMAL")

        print()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nFlight simulation ended.")
    print(f"Flight data saved to: {logFile}")

summarizeFlight(logFile)