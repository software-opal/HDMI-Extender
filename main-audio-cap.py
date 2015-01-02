#!/usr/bin/env python
from __future__ import print_function
import socket
import struct
import select
import time
import sys
import datetime

AUDIO_PORT = 2066

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
net = lambda pkt, idx: ord(pkt[idx]) * 0x100 + ord(pkt[idx + 1])

curr_time = datetime.datetime.utcnow()

file_name = "audio-backups-{:%Y-%m-%d_%H-%M-%S-%f}-.avi".format(curr_time)
print(file_name)
# output = av.open(file_name, 'w')



# audio_stream = output.add_stream("flac")
# resampler = av.AudioResampler(
#                        format=av.AudioFormat("s32"),
#                        layout="stereo",
#                        rate=48000)




# Audio Details.
# 2 Chanels
# 48000 Sample rate
# 32-bit big edian.

# To play through VLC:
# sudo python main-audio-cap.py | vlc --demux=rawaud --rawaud-channels 2 --rawaud-samplerate 48000 --rawaud-fourcc s32b -

data_start = 0x2a
while 1 > 0 :
    pkt = sock.recv(4096)


    is_udp = ord(pkt[23]) == 17

    if is_udp:
        src_port = net(pkt,34)
        dst_port = net(pkt,36)

        if src_port == dst_port == 2066:
            audio = pkt[data_start + 16:]
            sys.stdout.write(audio)
