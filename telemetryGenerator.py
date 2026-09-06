import random
random.seed(42)
from datetime import datetime, timezone



# telemetry = {
#     'altitude': 5000, #feet
#     'speed': 120, #mph
#     'battery': 100, #percent
#     'temp': 75, # C
# }

def generateTelemetry(previous):
    newTelemetry = previous.copy()

    # simulate changes in telemetry data
    newTelemetry["timestamp"] = datetime.now(timezone.utc).isoformat()
    newTelemetry['altitude'] += random.randint(-100, 100)
    newTelemetry['speed'] += random.randint(-5, 5)
    newTelemetry['battery'] -= random.uniform(0.1, 0.5)
    newTelemetry['temp'] += random.uniform(-1, 1)

    return newTelemetry
