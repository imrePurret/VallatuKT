import numpy as np
import serial
import time

ser1 = serial.Serial('COM4', 115200)
ser1.write('?\n')
ser1.write('sd50\n')
