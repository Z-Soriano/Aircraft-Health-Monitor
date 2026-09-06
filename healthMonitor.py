def checkHealth(telemetry):
    warnings = []

    if telemetry['battery'] < 20:
        warnings.append("Battery level is below 20%")
    if telemetry['temp'] > 85:
        warnings.append("Temperature is above 85°C")
    if telemetry['altitude'] < 1000:
        warnings.append("Altitude is below 1000 feet")
    if telemetry['speed'] > 200:
        warnings.append("Speed is above 200 mph")

    return warnings
