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
            if confidence > 0.5:
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
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(frame, class_ids[i], confidences[i], round(
            x), round(y), round(x+w), round(y+h))

    cv2.imwrite("currentFrame.jpg", frame)

    #################################

    ######## PROCESSING #####

    f = open('isThereTrash.txt', 'w')
    f.write("true")
    f.close()

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
