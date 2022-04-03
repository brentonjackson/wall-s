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
vs = VideoStream(src=-1).start()
delay = 1  # send frames every 5 seconds to reduce load
time.sleep(2.0)

while True:
    # read frame from camera and save it on raspberry pi
    frame = vs.read()
    cv2.imwrite("currentFrame.jpg", frame)
    #img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #stop_data = cv2.CascadeClassifier('')

    # found = stop_data.detectMultiScale(img_gray,
    #                                minSize =(20, 20))

    # we found the motor position
    # call the arduino

    # send image to server and
    # save response from server processing
    commands = sender.send_image(rpiName, frame)

    # f = open('positionData.txt', 'w')
    # f.write(position.decode())
    # f.close()
    """
    how commands work:
        first byte:   motor -> location    off  
        second byte:  arm   -> open close  off
        third byte:   steer -> angle       off
    """
    write_read(commands.decode())
    
    
    # recieve.data
    # if not objects in data:
  #      ardunio.goforward
  #  else:
  #      arduino.motor1(pos1)
  #      arduino.motor2(pos2)

    time.sleep(delay)
