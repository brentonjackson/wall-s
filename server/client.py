# Program on client (raspberry pi) to stream video
# from webcam and send frames to server over
# network via ImageZMQ

# imports
# videostream to grab frames from camera
# argparse to process server ip address via command line
# socket to get pi hostname
# time to delay camera feed
# Importing Libraries
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import serial
import time
import cv2


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))


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
vs = VideoStream(src=0).start()
delay = 5  # send frames every 5 seconds to reduce load
time.sleep(2.0)
while True:
    # read frame from camera and save it on raspberry pi
    frame = vs.read()
    cv2.imwrite("currentFrame.jpg", frame)

    # send image to server and
    # save response from server processing
    commands = sender.send_image(rpiName, frame)

    """
    how commands work:
        first int:   motor -> location    off  
        second int:  arm   -> open close  off
        third int:   steer -> angle       off
    """
    write_read(commands.decode())
    time.sleep(delay)
