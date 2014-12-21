import socket
import struct
import select
import time
import sys

AUDIO_PORT = 2066

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)


print "Starting"
while 1 > 0 :
    data = sock.recv(4096)[42:]

    # header = data[0:16] # Should be 005555...5500000000

    audio = data[16:]
    sys.stdout.write(audio)
