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
    #cv2.imshow("cam-test",imgthreshold)
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
	    otse(ser1,ser2,'0')
	    otse(ser1,ser3,'0')
	    ser1.write('fs1\n')
	    ser2.write('fs1\n')
	    ser3.write('fs1\n')
            sys.exit()
        return koord
    
def punkt_kaugus(a1,a2,b1,b2):#funktsioon kahe punkti kauguse leidmiseks
        return (math.sqrt((a1-b1)**2 +(a2-b2)**2))    

def nega(a):#et mu deviations list ei laheks negatiivseks ega ule lubatud piiride
    for i in range(3):
        if a[i]<0: a[i]=0
        if a[i]>255: a[i]=255
    return a

def drive(threadName, delay):
    while True:
    	if koord[0][0]==0:
	    vasakule(ser2,ser3,'10')
	    t1 = 0.1*(int(180/koord[0][1]) + int(5-abs(koord[0][0])/60))
	    time.sleep(t1)
	    vasakule(ser2,ser3,'0')
	elif koord[0][0]>350:
	    print 'paremale'
	    paremale(ser1,ser3,'10')
	    t1 = 0.1*(int(180/koord[0][1]) + int(5-abs(koord[0][0]-320)/60))
	    time.sleep(t1)
	    paremale(ser1,ser3,'0')
	elif 290>koord[0][0]:
	    print 'vasakule'
	    vasakule(ser2,ser3,'10')
	    t1 = 0.1*(int(180/koord[0][1]) + int(5-abs(koord[0][0])/60))
	    time.sleep(t1)
	    vasakule(ser2,ser3,'0')
        else:
	    print 'otse'
	    if koord[0][1]>150:
		otse(ser1,ser2, '13')
            elif koord[0][1]>200:
                otse(ser1,ser2, '12')
            elif koord[0][1]>250:
                otse(ser1,ser2, '10')
	    elif koord[0][1]>300:
		otse(ser1,ser2,'9')
	    else:
		otse(ser1,ser2, '15')
	    t1 = 0.1*(1+int(float(sys.argv[2])/koord[0][1]))
	    time.sleep(t1)
	    otse(ser1,ser2, '0')

def otse(ser1,ser2, dist):
	ser1.write('sd'+dist+'\n')
	ser2.write('sd'+dist+'\n')

def vasakule(ser2,ser3):
	ser2.write('sd'+str(dist)+'\n')
	ser3.write('sd-'+str(dist)+'\n')

def paremale(ser1,ser3):
	ser1.write('sd'+str(dist)+'\n')
        ser3.write('sd-'+str(dist)+'\n')

ser1 = serial.Serial('/dev/ttyACM2')
ser1.write('?\n')
ser2 = serial.Serial('/dev/ttyACM0')
ser2.write('?\n')
ser3 = serial.Serial('/dev/ttyACM1')
ser3.write('?\n')
ser1.write('fs0\n')
ser2.write('fs0\n')
ser3.write('fs0\n')


varv_b = int(float(25))
varv_g = int(float(55))
varv_r = int(float(193))
r_dev_b = int(float(20))
r_dev_g = int(float(30))
r_dev_r = int(float(40))

lower = []
higher= []

lower.append(varv_b-r_dev_b), lower.append(varv_g-r_dev_g), lower.append(varv_r-r_dev_r)
higher.append(varv_b+r_dev_b), higher.append(varv_g+r_dev_g), higher.append(varv_r+r_dev_r)

lower = nega(lower)
higher = nega(higher)

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
    ch = cv2.waitKey(5)
    loendur+=1
    
    s, img = cam.read()
    leia(img,lower, higher)
    cv2.circle(img,(koord[0][0], koord[0][1]), 15, (255,255,255), 25)#ringjoon keskkoha jaoks

    kiri = "Koordinaat: "
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
    number1 = number
    
    if ch == 27:
        ch = cv2.waitKey(5)
        drive_thread.stop()
	otse(ser1,ser2,'0')
	otse(ser1,ser3,'0')
	ser1.write('fs1\n')
	ser2.write('fs1\n')
	ser3.write('fs1\n')
        sys.exit()
        break
 
cv2.destroyAllWindows()
