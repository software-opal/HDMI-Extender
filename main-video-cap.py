
from __future__ import print_function

import socket
import struct
import select
import sys
import os
import cv2
import numpy as np
import datetime
import time

MAGIC_PACKET_NO = 0x8000



def handle_partial_packet(pkts, f_no, p_no):
    return # I don't care about dropping packets.
    # But this is the code I might use if I did care.
    frame = "".join(pkts)
    if p_no >= MAGIC_PACKET_NO:
        f = open("partial-frames/{:d} - last - (revd {:d}) > (reqd {:d}).jpeg".format(f_no, len(pkts), last_pkt_no), "w")
    else:
        f = open("partial-frames/{:d} - first - (revd {:d}) > (reqd {:d}).jpeg".format(f_no, len(pkts), last_pkt_no), "w")
    f.write(frame)
    f.close()

def handle_full_packet(pkts, curr_frame, curr_pkt_no):
    frame = "".join(pkts)
    display_frame(frame)
    # TODO save to file and produce stream
    save_frame(frame)
    # transmit_frame(frame)

if "-d" in sys.argv:
    def display_frame(frame):
        try:
            i = cv2.imdecode(np.fromstring(frame, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
            cv2.imshow('i',i)
            k = cv2.waitKey(1)
            if k == 27:
                exit(0)
            if k == 32:
                f = open("f-{:d}.jpeg".format(f_no), "w")
                f.write(frame)
                f.close()
        except:
            pass
else:
    display_frame = lambda frame: None


TIME_10_MINS = datetime.timedelta(seconds=60)
output = (datetime.datetime.utcfromtimestamp(0),None)
frames = 100

def rotate_file():
    global output, frames
    open_time, file = output
    curr_time = datetime.datetime.utcnow()
    if open_time + TIME_10_MINS < curr_time:
    # if frames > 5:
        # TODO rotate.
        if file:
            file.flush()
            file.close()
        new_file = open("backups-{:%Y-%m-%d_%H.%M.%S.%f}-.mjpg".format(curr_time), "wb")
        output = (curr_time, new_file)
        # print("File: {:s}".format(file))
        # fps = (frames + 1) / (curr_time - open_time).total_seconds()
        #
        # print("FPS:  {:f}".format(fps))
        frames = 0


def save_frame(frame):
    rotate_file()
    global frames
    frames += 1
    output[1].write(frame)
    output[1].flush()






















sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)


net = lambda pkt, idx: ord(pkt[idx]) * 0x100 + ord(pkt[idx + 1])

pkts = []
last_packet_no = -1

# os.mkdir("partial-frames")


while 1 > 0 :

    pkt = sock.recv(4096)

    is_udp = ord(pkt[23]) == 17

    if is_udp:
        src_port = net(pkt,34)
        dst_port = net(pkt,36)

        if src_port == dst_port == 2068:
            f_no = net(pkt,42)
            p_no = net(pkt,44)

            if p_no == 0:
                if len(pkts) > 0:
                    handle_partial_packet(pkt, f_no, p_no)
                pkts = []

            data = pkt[46:]
            pkts.append(data)

            if p_no > 32768:
                last_pkt_no = p_no - 32768
                if len(pkts) != last_pkt_no + 1:
                    handle_partial_packet(pkts, f_no, p_no)
                else:
                    handle_full_packet(pkts, f_no, p_no)
                pkts = []





    # ethHeader = pkt[0][0:14]
    # ipHeader = pkt[0][14:34]
    # tcpHeader = pkt[0][34:54]
    #
    # ethH = struct.unpack("!6s6s2s",ethHeader)
    # ethdata = processEth(ethH)
    #
    # ipH = struct.unpack("!12s4s4s",ipHeader)
    # ipdata = processIP(ipH)
    #
    # tcpH = struct.unpack("!HH16", tcpHeader)
    # tcpdata = processTCP(tcpH)
    #
    # print "S.mac "+ethdata[0]+" D.mac "+ethdata[1]+"     from:  "+ipdata[0]+":"+tcpdata[0]+"    to:  "+ipdata[1]+":"+tcpdata[1]
    #time.sleep(1);
