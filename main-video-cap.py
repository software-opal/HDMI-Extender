#!/usr/bin/env python 
from __future__ import print_function

import socket
import sys
import cv2
from PIL import Image
import datetime
import av
from cStringIO import StringIO


MAGIC_PACKET_NO = 0x8000
VIDEO_FPS = 30
TIME_10_MINS = datetime.timedelta(seconds=60)

import logging

logging.basicConfig(level=logging.DEBUG)

# Promiscuous mode::

# ifconfig eth1 promisc

def handle_partial_packet(pkts, f_no, p_no):
    print("Dropped Packet", f_no)
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
    # image = cv2.imdecode(np.fromstring(frame, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

#    f = open("file" + str(curr_frame) + ".jpeg", "wb")

#    f.write(frame)
#    f.close()

    print(curr_frame, " - Has been recieved.")

    frame_io = StringIO(frame)
    image = Image.open(frame_io)
    # print(image)
    display_frame(frame, image)
    # TODO save to file and produce stream
    save_image_frame(frame, image)
#    transmit_frame(frame)

print(sys.argv)

if "-d" in sys.argv:
    def display_frame(frame, image):
        # try:
            cv2.imshow('i',image)
            k = cv2.waitKey(1)
            if k == 27:
                exit(0)
            if k == 32:
                # Space saves the image
                f = open("f-{:d}.jpeg".format(f_no), "w")
                f.write(frame)
                f.close()
        # except:
        #     pass
else:
    display_frame = lambda frame, image: None


class MediaWriter(object):


    def __init__(self):
        self.update_time = datetime.datetime.utcfromtimestamp(0)
        self.video_output = None
        self.video_stream = None
        self.audio_file = None
        self.frames = 0
        self.width = 0
        self.height = 0


    def write_image_frame(self, jpeg_frame, image):
        curr_time = datetime.datetime.utcnow()
        # h, w = image.shape[:2]
        w, h = image.size
        if self.update_time + TIME_10_MINS < curr_time \
           or self.width != w \
           or self.height != h:
            print("Frames: ", self.frames)
            # Time's up or image size has changed.
            self.force_rotate_file(curr_time)

            self.video_stream.width = self.width = w
            self.video_stream.height = self.height = h
            self.frames += 1
        # frame = av.VideoFrame.from_image(image)
        frame = av.VideoFrame(w, h, 'rgb24')
        frame.planes[0].update_from_string(image.tostring())
        packet = self.video_stream.encode(frame)
        self.video_output.mux(packet)


    def write_audio_frame(self, raw_audio):
        # TODO write this into the video so that it is all combined.
        if not self.audio_file:
            self.force_rotate_file()
        self.audio_file.write(raw_audio)
        self.audio_file.flush()


    def force_rotate_file(self, curr_time=None):
        if not curr_time:
            curr_time = datetime.datetime.utcnow()
        self.close_file()
        self.open_file(curr_time)
	self.frames = 0


    def close_file(self):
        if self.video_output:
            # The following while loops output any remaining frames.
            # Just incase they were cached.
            while True:
                packet = self.video_stream.encode()
                print("Cleanup", packet)
                if packet:
                    self.video_output.mux(packet)
                else:
                    break
            # while True:
            #     packet = self.audio_stream.encode()
            #     print("Cleanup", packet)
            #     if packet:
            #         self.output.mux(packet)
            #     else:
            #         break
            self.video_output.close()
        if self.audio_file:
            self.audio_file.close()


    def open_file(self, curr_time):
        base_file_name = "backups-{:%Y-%m-%d_%H-%M-%S-%f}-".format(curr_time)
        print(base_file_name)
        self.video_output = av.open(base_file_name + ".avi", 'w')

        self.video_stream = self.video_output.add_stream("mjpeg", VIDEO_FPS)
        self.video_stream.pix_fmt = "yuvj422p"
        bit_rate = 1024 * 1024 * 80 # The higher the better - this seems to be good from a quality perspective.
        self.video_stream.bit_rate = bit_rate
        self.video_stream.bit_rate_tolerance = bit_rate / 8

        # self.audio_stream = self.output.add_stream("pcm_s32be")
        # self.resampler = av.AudioResampler(
        #                     format=av.AudioFormat(args.format or stream.format.name).packed if args.format else None,
        #                     layout=int(args.layout) if args.layout and args.layout.isdigit() else args.layout,
        #                     rate=args.rate,
        #                     ) if (args.format or args.layout or args.rate) else None

        self.audio_file = open(base_file_name + ".raw", "wb")

        self.update_time = curr_time


output = MediaWriter()


def save_image_frame(frame, image):
    output.write_image_frame(frame, image)















raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)

net = lambda packet, idx: ord(packet[idx]) * 0x100 + ord(packet[idx + 1])

pkts = []
last_packet_no = -1

print("Note: All audio is 2-channel raw audio, uses 32-bits big endian and is taken at 48000Hz.")


while True:
    pkt = raw_socket.recv(4096)
    print("RCVD")
    is_udp = ord(pkt[23]) == 17

    if is_udp:
        src_port = net(pkt, 34)
        dst_port = net(pkt, 36)

        if src_port == dst_port == 2068:
            # Start Video Processing
            f_no = net(pkt, 42)
            p_no = net(pkt, 44)

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
            # End Video
        if src_port == dst_port == 2066:
            # End Video Processing

            pass
