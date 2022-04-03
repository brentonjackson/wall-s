# Program on server (macbook) to get video
# streams and display/process them

import cv2
import ctypes
import imagezmq
from PIL import Image, ImageOps
import numpy as np



imageHub = imagezmq.ImageHub()
# initialize neural network stuff #


###################################


while True:
    # receive frame and acknowledge receipt
    rpiName, frame = imageHub.recv_image()

    # cv2.imshow('recieved cap',frame) 
    kernel = np.ones((5,5), np.uint8)

    erosion = cv2.erode(frame, kernel, iterations = 1)

    opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

    closing = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

    
    cv2.imwrite("close.jpg", closing)
    cv2.imwrite("open.jpg", opening)
    cv2.imwrite("erosion.jpg", erosion)


   

    ########### PROCESS FRAME #######

    #image = Image.fromarray(frame)
    #st.image(image, use_column_width=True)

    #################################

    """      
    how commands work:
        first int:   motor -> location    off  
        second second:  arm   -> open close  off
        third byte:   steer -> angle       off
    
    openARM 0x0F
    closeARM 0x1F
    """
    motor = input("motor: ")
    arm = input("arm: ")
    steer = input("steer: ")


    commands = [float(motor), float(arm), float(steer)]
    imageHub.send_reply(bytes(str(commands), 'UTF-8'))
    print(f'sent {motor} {arm} {steer}')

