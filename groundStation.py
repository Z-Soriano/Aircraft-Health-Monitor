import socket
import json 

from healthMonitor import checkHealth
from flightLogger import createFlightLog, saveReading
from flightSummary import summarizeFlight

from jsonschema import FormatChecker, validate
from jsonschema.exceptions import SchemaError, ValidationError
jsonSchema = {
    "type": "object",
    "properties": {
        "sequenceNumber": {
            "type": "integer",
            "minimum": 1
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "altitude": {
            "type": "number",
            "minimum": 0,
            "maximum": 100000
        },
        "speed": {
            "type": "number",
            "minimum": 0
        },
        "battery": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "temp": {
            "type": "number",
            "minimum": -50,
            "maximum": 150
        }
    },
    "required": [
        "sequenceNumber",
        "timestamp",
        "altitude",
        "speed",
        "battery",
        "temp"
    ],
    "additionalProperties": False
}
def validateMessage(message):
    try:
        messageDict = json.loads(message)

        validate(
            instance=messageDict,
            schema=jsonSchema,
            format_checker=FormatChecker()
        )

    except json.JSONDecodeError as error:
        print(f"Syntax Error: Invalid JSON -> {error.msg}")
        return None

    except ValidationError as error:
        print(f"Data Error: Invalid telemetry -> {error.message}")
        return None

    except SchemaError as error:
        print(f"Schema Error: The validation schema is incorrect -> {error.message}")
        return None

    print("Telemetry message is valid.")
    return messageDict
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
bufferSize = 1024

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# binds socket to specified ip and port
sock.bind((UDP_IP, UDP_PORT))

sock.settimeout(1.0)

print("Ground Station server up and listening")

highestSequenceNumber = None
logFile = createFlightLog()
print(f"Saving flight data to: {logFile}")
# try to receive data in a loop, and handle KeyboardInterrupt for shutdown
try:
    while True:
        # recvfrom() blocks until data arrives
        try:
            data, addr = sock.recvfrom(bufferSize)
            message = data.decode("utf-8")
            messageDict = validateMessage(message)
            if messageDict is None:
                continue
            # print(f"Received message from {addr}: \n {messageDict}")
            warnings = checkHealth(messageDict)
            # print(
            #     f"Time: {messageDict['timestamp']} | "
            #     f"Altitude: {messageDict['altitude']:.1f} ft | "
            #     f"Speed: {messageDict['speed']:.1f} mph | "
            #     f"Battery: {messageDict['battery']:.1f}% | "
            #     f"Temperature: {messageDict['temp']:.1f}°C"
            # )

            sequenceNumber = messageDict.get("sequenceNumber")
            if highestSequenceNumber is None:
                print(f"Received first sequence: {sequenceNumber}")
            elif sequenceNumber == highestSequenceNumber + 1:
                print(f"Received expected sequence: {sequenceNumber}")

            elif sequenceNumber > highestSequenceNumber + 1:
                expectedSequenceNumber = highestSequenceNumber + 1
                missingCount = sequenceNumber - expectedSequenceNumber
                print(
                    f"WARNING: Expected sequence {expectedSequenceNumber}, "
                    f"but received {sequenceNumber}. "
                    f"Possibly missed {missingCount} message(s)."
                )
            elif sequenceNumber < highestSequenceNumber + 1:
                print(f"Out of order sequence, expected: {highestSequenceNumber+1}, but received {sequenceNumber}.")
                continue
            else:
                print(f"Expected sequence number {highestSequenceNumber+1}, but received {sequenceNumber}.")
            highestSequenceNumber = sequenceNumber
            saveReading(logFile, messageDict, warnings)

        # continue loop if timeout occurs, this allows a constant refresh and check for KeyboardInterrupt
        except socket.timeout:
            continue
except KeyboardInterrupt:
    print("\nReceiver shutting down immediately.")
    print(f"Flight data saved to: {logFile}")
finally:
    sock.close()   

summarizeFlight(logFile)