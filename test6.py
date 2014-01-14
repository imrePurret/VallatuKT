import numpy as np
import serial
import time

ser1 = serial.Serial('COM6')
while True:
        ser1.write('1\n')
        time.sleep(0.7)
