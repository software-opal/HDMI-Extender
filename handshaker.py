from __future__ import print_function
import socket
import time

resp_online_ = "54:46:36:7A:60:02:00:00:00:00:00:03:03:01:00:26:00:00:00:00:02:34:C2"
response_hex = "54:46:36:7a:60:02:00:00:5d:3e:00:03:03:01:00:26:19:19:00:00:f5:a2:31:00"
data = ""
for hexdec in resp_online_.split(":"):
    data += chr(int(hexdec, 16))

# FROM_IP = "226.2.2.2"
PORT = 48689

TO_IP = "192.168.168.55"


to_rcvr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

to_rcvr.bind(("0.0.0.0", PORT))

while 1 > 0:
    print("Sending")
    to_rcvr.sendto(data, (TO_IP, PORT))
    time.sleep(1)
