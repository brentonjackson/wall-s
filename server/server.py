# Program on server (macbook) to get video
# streams and display/process them

import cv2
import imagezmq
from PIL import Image, ImageOps
import numpy as np

imageHub = imagezmq.ImageHub()
# initialize neural network stuff #


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1]
                     for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x-10, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


classes = None
with open('ml_classes.txt', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNet('ml.weights', 'ml.cfg')

class_ids = []
confidences = []
boxes = []
conf_threshold = 0.9
nms_threshold = 0.4
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
