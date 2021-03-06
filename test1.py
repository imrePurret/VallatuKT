import numpy as np
import cv2
import colorsys
from time import sleep
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
            sys.exit()
        return koord
    
def punkt_kaugus(a1,a2,b1,b2):#funktsioon kahe punkti kauguse leidmiseks
        return (math.sqrt((a1-b1)**2 +(a2-b2)**2))    

def nega(a):#et mu deviations list ei laheks negatiivseks ega ule lubatud piiride
    for i in range(3):
        if a[i]<0:
            a[i]=0
    for i in range(3):
        if a[i]>255:
            a[i]=255
    return a

def otse(ser1,ser2,dist):
        ser1.write('sd'+dist+'\n')
        ser2.write('sd'+dist+'\n')

def vasakule(ser3,dist):
	ser3.write('sd'+dist+'\n')

def paremale(ser3,dist):
        ser3.write('sd-'+dist+'\n')

ser1 = serial.Serial('/dev/ttyACM2', 115200)
ser1.write('?\n')
ser1.write('dr1\n')
ser2 = serial.Serial('/dev/ttyACM0', 115200)
ser2.write('?\n')
ser2.write('dr0\n')
ser3 = serial.Serial('/dev/ttyACM1', 115200)
ser3.write('?\n')



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
        break
    if loendur%30==0:
	if koord[0][0]==0:
	    vasakule(ser3,'8')
	    otse(ser1,ser2,'8')
	elif koord[0][0]>350:
	    print 'paremale'
	    if koord[0][0]>410:
		paremale(ser3,'6')
	    else:
	        paremale(ser3,'5')
	elif 290>koord[0][0]:
	    print 'vasakule'
	    if 230>koord[0][0]:
		vasakule(ser3,str('6'))
	    else:
	        vasakule(ser3,str('5'))
        else:
	    print 'otse'
	    otse(ser1,ser2,'6')   
cv2.destroyAllWindows()
