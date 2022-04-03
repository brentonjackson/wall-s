# Program on server (macbook) to get video
# streams and display/process them

import cv2
import imagezmq
from PIL import Image, ImageOps
import numpy as np

imageHub = imagezmq.ImageHub()
# initialize neural network stuff #


###################################


while True:
    # receive frame
    rpiName, frame = imageHub.recv_image()

    ########### PROCESS FRAME #######

    image = Image.fromarray(frame)
    #st.image(image, use_column_width=True)

    #################################

    ######## PROCESSING #####

    f = open('isThereTrash.txt', 'w')
    f.write("true")
    f.close()

    cv2.imshow(rpiName, frame)
    cv2.imwrite("../client/public/images/currentFrame.jpg", frame)

    ##################################
    # send position back to raspberry pi
    x = 5
    imageHub.send_reply(str(x).encode())

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# cleanup
cv2.destroyAllWindows()
