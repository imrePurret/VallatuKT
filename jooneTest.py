import numpy as np
import serial
import time


ser1 = serial.Serial('/dev/ttyACM4')
while True:
	print(ser1.readline())
	ser1.write('1\n')
