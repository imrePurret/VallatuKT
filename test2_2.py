import numpy as np 
import cv2 
import colorsys 
import thread 
import threading 
import math 
import sys 
import time 
import timeit 
import serial 
from datetime import datetime


global ser1
global ser2
global ser3
ser1 = serial.Serial('/dev/ttyACM2')
ser1.write('?\n')
ser1.write('fs0\n')
ser2 = serial.Serial('/dev/ttyACM0')
ser2.write('?\n')
ser2.write('fs0\n')
ser3 = serial.Serial('/dev/ttyACM1')
ser3.write('?\n')
ser3.write('fs0\n')
serA = serial.Serial('/dev/ttyACM3')
serA.write('?\n')

#ora_lower = [5,25,153]
#ora_higher = [45,85,233]

ora_lower = [0,40,153]
ora_higher = [15,87,233]

#blu_lower = [90,63,0]
#blu_higher = [130,93,74]

blu_lower = [67,34,17]
blu_higher = [100,49,25]

#yel_lower = [30,145,140]
#yel_higher = [85,170,180]

yel_lower = [35,129,129]
yel_higher = [71,166,180]

bla_lower = [65,85,69]
bla_higher = [90,121,103]

#Yellow goal Red - 234 Green - 205 Blue - 15

#Blue goal Red - 34 Green - 43 Blue - 110

#Ball Red - 193 Green - 55 Blue - 25

cam = cv2.VideoCapture(int(float(sys.argv[1])))   # 0 -> index of camera
s, img = cam.read()
global koord
global abiK

if s:    # frame captured without any errors
    cv2.namedWindow("cam",cv2.CV_WINDOW_AUTOSIZE)
    cv2.moveWindow("cam",10,10)

koord = [(0,0)]
abiK = [(0,0)]
number1 = [0,0]
kiirus_kesk = 0

def leia2(image, lower,higher, vert, hori):#leian roboti kontuurjooned, mille jargi saab keskkoha teada
    global koord
    imgthreshold=cv2.inRange(image.copy(),np.uint8(lower),np.uint8(higher))
    contours,hierarchy=cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    b = len(contours)

    pikkus = []
    #print len(contours)
    if (b)!=0:
        for i in range(b):
	    if hori+15<contours[i][0][0][1]:
            	a = len(contours[i])
            	pikkus.append(a)
        if len(pikkus)==0:
	    return
        milline = pikkus.index(max(pikkus))#tagastan ainult suurima kontuurpunktide arvuga kujundi
        x =(np.sum(contours[milline], axis = 0)[0])/len(contours[milline])
	koord = []
        koord.append(x)	
        return koord

def leia(image, lower,higher):#leian roboti kontuurjooned, mille jargi saab keskkoha teada
    global abiK
    imgthreshold=cv2.inRange(image.copy(),np.uint8(lower),np.uint8(higher))
    contours,hierarchy=cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    b = len(contours)

    pikkus = []
    #print len(contours)
    if (b)!=0:
        longestElement = max(contours, key=len)
        x =(np.sum(longestElement, axis = 0)[0])/len(longestElement)
        abiK = []
        abiK.append(x)
        return abiK
    else:
	abiK = [(0,0)]

    
def punkt_kaugus(a1,a2,b1,b2):#funktsioon kahe punkti kauguse leidmiseks
        return (math.sqrt((a1-b1)**2 +(a2-b2)**2))

def allSpeedsToZero():#Funktsioon paneb koigi rataste kiiruse nulli ja paneb peale automaatse mootorite peatamise.
    ser1.write('sd0\n')
    ser2.write('sd0\n')
    ser3.write('sd0\n')

def allMotorAutomatic():
    ser1.write('fs1\n')
    ser2.write('fs1\n')
    ser3.write('fs1\n')


def drive(threadName, stop_event):
    global koord
    time.sleep(0.1)
    while(not stop_event.is_set()):
    	if len(koord) == 0:
	    time.sleep(0.0001)
	elif koord[0][0]==0:
	    setSpeed(ser1,ser3,'-0','-13')
	    t1 = 0.015*(int(koord[0][1]/90) + int(29-abs(koord[0][0])/10))
	    time.sleep(max(t1,0.25))
	    print t1
	    setSpeed(ser1,ser3,'0','0')
	    time.sleep(0.05)
	if koord[0][0]>390 or (360<koord[0][0] and koord[0][1]>180):
	    print 'paremale'
	    setSpeed(ser2,ser3,'-0','20')
	    t1 = 0.008*(int(koord[0][1]/90) + int(abs(koord[0][0]-320)/10))
	    time.sleep(max(t1,0.19))
	    print t1
	    setSpeed(ser2,ser3,'0','0')
	    time.sleep(0.05)
	elif 250>koord[0][0] or (280>koord[0][0] and koord[0][1]>180):
	    print 'vasakule'
	    setSpeed(ser1, ser3,'-0', '-20')
	    t1 = 0.008*(int(koord[0][1]/90) + int(32-abs(koord[0][0])/10))
	    time.sleep(max(t1,0.19))
	    print t1
	    setSpeed(ser1,ser3,'0', '0')
	    time.sleep(0.05)
        else:
	    print 'otse'
	    t1=0
	    if koord[0][1]>100:
		setSpeed(ser1,ser2, '16', '16')
                t1 = 0.35
	    elif koord[0][1]>175:
		setSpeed(ser1,ser2, '11', '11')
	        t1 = 0.3
	    else:
		setSpeed(ser1,ser2, '18', '18')
	        t1 = 0.4
	    time.sleep(t1)
	    print t1
	    setSpeed(ser1,ser2, '0', '0')
	time.sleep(0.05)

def setSpeed(ser_1,ser_2, dist1, dist2):
	ser_1.write('sd'+dist1+'\n')
	ser_2.write('sd'+dist2+'\n')

def setSpeedT(ser_3, dist):
	ser_3.write('sd'+dist+'\n')
def lineChecker(threadName, stop_event):
        while True:
		anb = serA.readline()
        	#print(anb)
#		if anb != 0:
		#	print("Ei ole null")

t2_stop= threading.Event()

drive_thread = thread.start_new_thread( lineChecker, ("Thread-2", t2_stop))

def find_ball():
    global koord
    number1 = [0,0]
    kiirus_kesk = 0
    loendur = 0
    l = 0
    t1_stop= threading.Event()
    print "find ball"
    while True:
        if l == 0:
            start = datetime.now()#fps esimese kaadri jaoks
        if loendur == 2:
            drive_thread = thread.start_new_thread( drive, ("Thread-1", t1_stop))        
        ch = cv2.waitKey(5)
        loendur+=1
        
        s, img = cam.read()
#        leia(img, bla_lower, bla_higher)
	leia2(img, ora_lower, ora_higher,abiK[0][0],abiK[0][1])
        cv2.circle(img,(koord[0][0], koord[0][1]), 15, (255,255,255), 25)#ringjoon keskkoha jaoks
        
        if koord[0][1]>int(float(sys.argv[2])) and koord[0][0]>290 and 350>koord[0][0]:
            print "ball found"
	    t1_stop.set()
	    setSpeed(ser1,ser2,'10','10')
            time.sleep(0.5)
            allSpeedsToZero()
            koord = [(0,0)]
            loendur = 0
            if sys.argv[3] == "y":
                find_goal(yel_lower, yel_higher)
            else:
                find_goal(blu_lower, blu_higher)
   	
    	kiri = "Koordinaat: "
    	number = [koord[0][1],koord[0][0]]
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
    	start = datetime.now()#fpsi mootmine alates teisest kaadristx
    	l = 1
    	fps = str( '%.2f' % (1000000.0/(aeg.microseconds)))
    	aeg_kokku =str(aeg_kiri+fps)
    
    
    	cv2.putText(img,aeg_kokku , (5,45), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#fps ekraanile
    
    	cv2.imshow("cam",img)
    	number1 = number


        if ch == 27:
            ch = cv2.waitKey(5)
	    t1_stop.set()
            allSpeedsToZero()
	    allMotorAutomatic()
            sys.exit()
            break	

def find_goal(c_lower, c_higher):
    global koord
    koord = [(0,0)]
    number1 = [0,0]
    kiirus_kesk = 0
    loendur = 0
    l = 0
    t2_stop= threading.Event()
    print c_lower
    print "find goal"
    while True:
        if loendur == 2:
            drive_thread = thread.start_new_thread( drive, ("Thread1", t2_stop))        
        ch = cv2.waitKey(5)
        loendur+=1
        
        s, img = cam.read()
        leia2(img, c_lower, c_higher,0,0)
        cv2.circle(img,(koord[0][0], koord[0][1]), 15, (255,255,255), 25)#ringjoon keskkoha jaoks
	cv2.imshow("cam", img)

        if koord[0][1]>int(float(75)) and koord[0][0]>240 and koord[0][0]<400:
            t2_stop.set()
	    serA.write('1\n')
	    setSpeed(ser1,ser2,'10','10')
            time.sleep(0.1)
	    setSpeed(ser1, ser3,'-0', '-20')
            time.sleep(0.5)
            allSpeedsToZero()
	    allMotorAutomatic()
	    koord = [(0,0)]
            loendur = 0
	    find_ball()

        if ch == 27:
            ch = cv2.waitKey(5)
	    t2_stop.set()
            allSpeedsToZero()
	    allMotorAutomatic()
            sys.exit()
            break

find_ball()    
 
cv2.destroyAllWindows()

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
    start = datetime.now()#fpsi mootmine alates teisest kaadristx
    l = 1
    fps = str( '%.2f' % (1000000.0/(aeg.microseconds)))
    aeg_kokku =str(aeg_kiri+fps)
    
    
    cv2.putText(img,aeg_kokku , (5,45), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#fps ekraanile
    
    cv2.imshow("cam-test",img)
    number1 = number'''
    



