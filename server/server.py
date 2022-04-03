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
    label = str(classes[class_id]) + " - " + \
        str(round(confidence*100, 2)) + "%"
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
conf_threshold = 0.95
nms_threshold = 0.1
###################################


while True:
    # receive frame
    rpiName, frame = imageHub.recv_image()

    ########### OBJECT DETECTION #######
    width = frame.shape[1]
    height = frame.shape[0]
    scale = 0.00392

    blob = cv2.dnn.blobFromImage(
        frame, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.8:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, conf_threshold, nms_threshold)
    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(frame, class_ids[i], confidences[i], round(
            x), round(y), round(x+w), round(y+h))

    num_objects = len(indices)

    cv2.imwrite("currentFrame.jpg", frame)

    ######## WEB SERVER PROCESSING ##########

    f = open('isThereTrash.txt', 'w')
    f.write("true")
    f.close()

    cv2.imwrite("../client/public/images/currentFrame.jpg", frame)

    ########## PI INTERFACING ##########

    """      
    how commands work:
        first int:   motor -> location    off  
        second second:  arm   -> open close  off
        third byte:   steer -> angle       off
    
    openARM 0x0F
    closeARM 0x1F
    """
    # motor = input("motor: ")
    # arm = input("arm: ")
    # steer = input("steer: ")

    # commands = [float(motor), float(arm), float(steer)]
    # imageHub.send_reply(bytes(str(commands), 'UTF-8'))

    # print(f'sent {motor} {arm} {steer}')

    imageHub.send_reply(b'OK')
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# cleanup
cv2.destroyAllWindows()
