# Program on server (macbook) to get video
# streams and display/process them

import cv2
import imagezmq
#import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

imageHub = imagezmq.ImageHub()
# initialize neural network stuff #


def predict_stage(image_data, model):
    size = (224, 224)
    image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
    image_array = np.array(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    preds = ""
    prediction = model.predict(data)
    return prediction

###################################


def fruit_price(arr):
    if (arr[0] > arr[1] and arr[0] > arr[2]):
        # Unripe
        return 10
    elif (arr[1] > arr[0] and arr[1] > arr[2]):
        # Overripe
        return 3
    else:
        # ripe
        return 6


while True:
    # receive frame and acknowledge receipt
    rpiName, frame = imageHub.recv_image()
    imageHub.send_reply(b'OK')

    ########### PROCESS FRAME #######

    #image = Image.fromarray(frame)
    #st.image(image, use_column_width=True)
    #model = tf.keras.models.load_model('ripeness.h5')
    #prediction = predict_stage(image, model)
    #probarr = prediction[0]
    #price = fruit_price(probarr)
    #print('THE PREDICTION IS ' + str(price))

    #################################

    ######## WEB APP PROCESSING #####

    # write price to file currentFruitPrice.txt
    f = open('currentFruitPrice.txt', 'w')
    # price = fruit_price(fruit_status)
    # price = random.choice([0.75, 1.00, 1.25, 2.00, 3.00])

    #print('random price: ', price)
    # f.write(str(price))
    f.write('test to david')
    f.close()

    #cv2.imshow(rpiName, frame)

    ##################################

    #key = cv2.waitKey(1) & 0xFF
    #if key == ord('q'):
 #       break

# cleanup
cv2.destroyAllWindows()
