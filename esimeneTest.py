import numpy as np
import serial
import time

def kraadi60(ds): #Kohapeal ringid
	ser1.write('sd-'+ds+'\n')
	ser3.write('sd'+ds+'\n')

def kraadi240(ds):
	ser1.write('sd'+ds+'\n')
	ser3.write('sd-'+ds+'\n')

def kraadi0(ds): # paremale ja natuke tagasi
        ser2.write('sd'+ds+'\n')
        ser3.write('sd'+ds+'\n')

def kraadi180(ds): #otse paremale
        ser2.write('sd-'+ds+'\n')
        ser3.write('sd-'+ds+'\n')

def kraadi120(ds): #otse tagasi
        ser1.write('sd-'+ds+'\n')
        ser2.write('sd-'+ds+'\n')

def kraadi300(ds): # otse edasi
        ser1.write('sd'+ds+'\n')
        ser2.write('sd'+ds+'\n')
def seisma():
	ser1.write('sd0\n')
	ser2.write('sd0\n')
	ser3.write('sd0\n')



ser1 = serial.Serial('COM3')
ser1.write('?\n')
ser1.write('fs1\n')
ser1.write('sd0\n')

ser2 = serial.Serial('COM7')
ser2.write('?\n')
ser2.write('fs1\n')
ser2.write('sd0\n')

ser3 = serial.Serial('COM9')
ser3.write('?\n')
ser3.write('fs1\n')
ser3.write('sd0\n')

kraadi120('30')
time.sleep(0.5)
seisma()

def paremale(ser1,ser3,dist):
	ser1.write('sd'+str(int(dist))+'\n')
        ser3.write('sd-'+str(dist)+'\n')
