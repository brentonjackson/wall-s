# Program on client (raspberry pi) to stream video
# from webcam and send frames to server over
# network via ImageZMQ

# imports
# videostream to grab frames from camera
# argparse to process server ip address via command line
# socket to get pi hostname
# time to delay camera feed
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

# construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
                help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

# initialize ImageSender object with socket address of server
sender = imagezmq.ImageSender(
    connect_to="tcp://{}:5555.".format(args["server_ip"]))

# get hostname, initialize video stream, and allow
# camera sensor to warmup
rpiName = socket.gethostname()
vs = VideoStream(src=-1).start()
delay = 5  # send frames every 5 seconds to reduce load
time.sleep(2.0)

while True:
    # read frame from camera and send to server
    frame = vs.read()
    # frame = imutils.resize(frame, width=320)
    sender.send_image(rpiName, frame)
    time.sleep(delay)
