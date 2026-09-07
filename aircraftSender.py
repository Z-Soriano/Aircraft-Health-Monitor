import socket
import json
import time

from telemetryGenerator import generateTelemetry


UDP_IP = "127.0.0.1"
UDP_PORT = 5005


# telemetry = {
#     "sequenceNumber": 0,
#     "altitude": 5000.0, 
#     "speed": 120.0,
#     "battery": 100.0,
#     "temp": 75.0
# }

telemetry = {
    "sequenceNumber": 8,
    "altitude": 500,
    "speed": 40,
    "battery": 10,
    "temp": 110
}

# 1. Convert dict to JSON string
jsonString = json.dumps(telemetry)

# 2. Convert JSON string to UTF-8 bytes
byteData = jsonString.encode('utf-8')

print(f"Target IP: {UDP_IP}")
print(f"Target Port: {UDP_PORT}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sequenceNumber = 1
try:
    while True:
        telemetry = generateTelemetry(telemetry)
        jsonMessage = json.dumps(telemetry)
        encodedMessage = jsonMessage.encode("utf-8")
        sock.sendto(encodedMessage, (UDP_IP, UDP_PORT))
        print(f"Sent telemetry: #{sequenceNumber}")
        print(f"Sending message: \n{telemetry}")


        sequenceNumber += 1
        time.sleep(1)
except KeyboardInterrupt:
    print("\nFlight simulation ended.")
