#!/usr/bin/env python 
from __future__ import print_function
import socket
import time

resp_online_ = "54:46:36:7A:60:02:00:00:00:00:00:03:03:01:00:26:00:00:00:00:02:34:C2:00"
response_hex = "54:46:36:7a:60:02:00:00:5d:3e:00:03:03:01:00:26:19:19:00:00:f5:a2:31:00"
resp = resp_online_
# resp = response_hex
data = ""
for hexdec in resp.split(":"):
    data += chr(int(hexdec, 16))

# FROM_IP = "226.2.2.2"
PORT = 48689

TO_IP = "192.168.168.55"


to_rcvr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

to_rcvr.bind(("0.0.0.0", PORT))

print("Bound & Sending")

while 1 > 0:
    _, sender = to_rcvr.recvfrom(40960)
    # Make it look like we care about what it is sending.
    to_rcvr.sendto(data, sender)
    time.sleep(0.9)
