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
import cv2

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
    #img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #stop_data = cv2.CascadeClassifier('')

    # found = stop_data.detectMultiScale(img_gray,
    #                                minSize =(20, 20))

    # we found the motor position
    # call the arduino

    # send image to server and
    # save response from server processing
    position = sender.send_image(rpiName, frame)

    # if we get a position from server, stop and go to that position
    # until all positions visited
    # else, go forward along path
    if position == b'OK':
        # move forward (control arduino)
        print(position)
    else:
        # go to position
        print(position)

    f = open('isThereTrash.txt', 'w')
    f.write("true")
    f.close()

    time.sleep(delay)
    # recieve.data
    # if not objects in data:
  #      ardunio.goforward
  #  else:
  #      arduino.motor1(pos1)
  #      arduino.motor2(pos2)

    # time.sleep(delay)
