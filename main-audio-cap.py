import socket
import struct
import select
import time

AUDIO_PORT = 2066

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)

# sock.bind(("0.0.0.0", AUDIO_PORT))
net = lambda pkt, idx: ord(pkt[idx]) * 0x100 + ord(pkt[idx + 1])

file = open("out.raw", "wb", 0)
print "Starting"
bytes_written = 0
stime = time.time()
try:
    while 1 > 0 :
        data = sock.recv(4096)[42:]

        header = data[0:16] # Should be 005555...5500000000

        audio = data[16:]
        bytes_written += len(audio)
        file.write(audio)
        
except KeyboardInterrupt:
    pass
print stime - time.time()
print bytes_written
sock.close()
