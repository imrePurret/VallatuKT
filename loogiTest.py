import numpy as np
import serial
import time


ser1 = serial.Serial('/dev/ttyACM3')
time.sleep(1)
ser1.write('1\n')
