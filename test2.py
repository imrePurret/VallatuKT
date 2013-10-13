import numpy as np
import cv2
import colorsys
from time import sleep
import thread
import time
import math
import sys
import timeit
import serial
from datetime import datetime


def leia(image, lower,higher):#leian roboti kontuurjooned, mille jargi saab keskkoha teada
    global koord
    imgthreshold=cv2.inRange(image.copy(),np.uint8(lower),np.uint8(higher))
    contours,hierarchy=cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    b = len(contours)

    pikkus = []
    #print len(contours)
    if (b)!=0:
        koord = []
	longestElement = max(contours, key=len)
	x =(np.sum(longestElement, axis = 0)[0])/len(longestElement)
        koord.append(x)
        if koord[0][1]>int(float(sys.argv[2])):
            allSpeedsToZero()
            sys.exit()
            return True
        return False
    
def punkt_kaugus(a1,a2,b1,b2):#funktsioon kahe punkti kauguse leidmiseks
        return (math.sqrt((a1-b1)**2 +(a2-b2)**2))

def allSpeedsToZero():
    ser1.write('sd0\n')
    ser2.write('sd0\n')
    ser3.write('sd0\n')
    ser1.write('fs1\n')
    ser2.write('fs1\n')
    ser3.write('fs1\n')

def drive(threadName, delay):
    while True:
    	if koord[0][0]==0:
	    #setSpeed(ser2,ser3,'10')
	    t1 = 0.05*(int(90/koord[0][1]) + int(9-abs(koord[0][0])/30))
	    time.sleep(t1)
	    setSpeed(ser2,ser3,'0')
	elif koord[0][0]>350:
	    print 'paremale'
	    setSpeed(ser1,ser3,'10')
	    t1 = 0.05*(int(90/koord[0][1]) + int(abs(koord[0][0]-320)/30))
	    time.sleep(t1)
	    setSpeed(ser1,ser3,'0')
	elif 290>koord[0][0]:
	    print 'vasakule'
	    setSpeed(ser2,ser3,'10')
	    t1 = 0.05*(int(90/koord[0][1]) + int(9-abs(koord[0][0])/30))
	    time.sleep(t1)
	    setSpeed(ser2,ser3,'0')
        else:
	    print 'otse'
	    if koord[0][1]>150:
		setSpeed(ser1,ser2, '13')
            elif koord[0][1]>200:
                setSpeed(ser1,ser2, '12')
            elif koord[0][1]>250:
                setSpeed(ser1,ser2, '10')
	    elif koord[0][1]>300:
		setSpeed(ser1,ser2,'9')
	    else:
		setSpeed(ser1,ser2, '15')
	    t1 = 0.1*(1+int(float(sys.argv[2])/(koord[0][1]+30)))
	    time.sleep(t1)
	    otse(ser1,ser2, '0')

def setSpeed(ser_1,ser_2, dist):
	ser_1.write('sd'+dist+'\n')
	ser_2.write('sd'+dist+'\n')
	
ser1 = serial.Serial('/dev/ttyACM2')
ser1.write('?\n')
ser1.write('fs0\n')
ser2 = serial.Serial('/dev/ttyACM0')
ser2.write('?\n')
ser2.write('fs0\n')
ser3 = serial.Serial('/dev/ttyACM1')
ser3.write('?\n')
ser3.write('fs0\n')

#Yellow goal
#Red - 234
#Green - 205
#Blue - 15

#Blue goal
#Red - 34
#Green - 43
#Blue - 110

#Ball
#Red - 193
#Green - 55
#Blue - 25

ora_lower = [5,25,153]
ora_higher = [45,85,233]

blu_lower = [90,13,0]
blu_higher = [130,73,74]

yel_lower = [0,175,194]
yel_higher = [35,235,255]

cam = cv2.VideoCapture(int(float(sys.argv[1])))   # 0 -> index of camera
loendur = 0
s, img = cam.read()
global koord

if s:    # frame captured without any errors
    cv2.namedWindow("cam-test",cv2.CV_WINDOW_AUTOSIZE)

koord = [(0,0)]
number1 = [0,0]
kiirus_kesk = 0
l = 0

while True:
    if l == 0:
        start = datetime.now()#fps esimese kaadri jaoks
    if loendur == 5:
	drive_thread = thread.start_new_thread( drive, ("Thread-1", 2))        
    ch = cv2.waitKey(50)
    loendur+=1
    
    s, img = cam.read()
    if leia(img,ora_lower, ora_higher):
        drive_thread.stop()
        break
    cv2.circle(img,(koord[0][0], koord[0][1]), 15, (255,255,255), 25)#ringjoon keskkoha jaoks

'''    kiri = "Koordinaat: "
    number = [koord[0][1],koord[0][0]]#siit edasi tulevad tesktid, mida kuvada
    tekst2 = str(number)
    kolmas = str(kiri+tekst2)
    koordiabi = tekst2
    
    frame = str(loendur)
    frame_kiri = "Frame: "
    frame_kokku = str(frame_kiri+frame)
    
    cv2.putText(img,kolmas , (5,15), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#koordinaadid
    
    cv2.putText(img,frame_kokku , (5,30), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#frame
    
    aeg_kiri = "FPS: "       
    end = datetime.now()#fpsi mootmise lopp
    aeg = end-start
    start = datetime.now()#fpsi mootmine alates teisest kaadrist
    l = 1
    fps = str( '%.2f' % (1000000.0/(aeg.microseconds)))
    aeg_kokku =str(aeg_kiri+fps)
    
    
    cv2.putText(img,aeg_kokku , (5,45), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#fps ekraanile
    
    cv2.imshow("cam-test",img)
    number1 = number'''
    
    if ch == 27:
        ch = cv2.waitKey(50)
        drive_thread.stop()
        allSpeedsToZero()
        sys.exit()
        break

koord = [(0,0)]
number1 = [0,0]
kiirus_kesk = 0

while True:
    if l == 0:
        start = datetime.now()
    if loendur == 5:
	drive_thread = thread.start_new_thread( drive, ("Thread-1", 2))        
    ch = cv2.waitKey(50)
    loendur+=1
    
    s, img = cam.read()
    if leia(img, blu_lower, blu_higher):
        drive_thread.stop()
        break
    cv2.circle(img,(koord[0][0], koord[0][1]), 15, (255,255,255), 25)#ringjoon keskkoha jaoks

    if ch == 27:
        ch = cv2.waitKey(50)
        drive_thread.stop()
        allSpeedsToZero()
        sys.exit()
        break
    
 
cv2.destroyAllWindows()
