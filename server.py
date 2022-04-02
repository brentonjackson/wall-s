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
    # receive frame and acknowledge receipt
    rpiName, frame = imageHub.recv_image()
    x = 5
    imageHub.send_reply(str(x).encode())

    ########### PROCESS FRAME #######

    image = Image.fromarray(frame)
    #st.image(image, use_column_width=True)

    #################################

    ######## WEB APP PROCESSING #####

    f = open('currentFruitPrice.txt', 'w')
    f.write('test to david')
    f.close()

    cv2.imshow(rpiName, frame)
    cv2.imwrite('VisionFrame.jpg', frame)

    ##################################

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# cleanup
cv2.destroyAllWindows()
