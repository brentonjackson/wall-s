# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(driveFORWARD, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    #calculate rotations

    num = 1
    value = write_read(num)
    print(value) # printing the value
