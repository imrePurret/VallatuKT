import numpy as np
import serial
import time

ser1 = serial.Serial('COM4', 115200)
#ser2 = serial.Serial('COM3', 115200)
ser1.write('?\n')
ser1.write('sd100\n')
#ser2.write('?\n')
#ser2.write('sd10\n')
