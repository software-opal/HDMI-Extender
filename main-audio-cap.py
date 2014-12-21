from __future__ import print_function
import socket
import struct
import select
import time
import sys

AUDIO_PORT = 2066

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
net = lambda pkt, idx: ord(pkt[idx]) * 0x100 + ord(pkt[idx + 1])

# Audio Details.
# 2 Chanels
# 48000 Sample rate
# 32-bit big edian.

# To play through VLC:
# sudo python main-audio-cap.py | vlc --demux=rawaud --rawaud-channels 2 --rawaud-samplerate 48000 --rawaud-fourcc s32b -

data_start = 0x28 + 0x02
while 1 > 0 :
    pkt = sock.recv(4096)


    is_udp = ord(pkt[23]) == 17

    if is_udp:
        src_port = net(pkt,34)
        dst_port = net(pkt,36)

        if src_port == dst_port == 2066:
            ip_header = pkt[0:data_start] # Should be 005555...5500000000
            audio_header = pkt[data_start:data_start + 16]

            # print([hex(ord(c)) for c in ip_header]
            # print [hex(ord(c)) for c in audio_header]
            print(len(pkt) - (data_start + 16), file=sys.stderr)

            audio = pkt[data_start + 16:]
            sys.stdout.write(audio)
