import numpy as np 
import cv2 
import colorsys 
import thread 
import threading 
import math 
import sys 
import operator
import time 
import timeit 
import serial 
from datetime import datetime
 

global ser1
global ser2
global ser3
ser1 = serial.Serial('COM3', baudrate=9600, writeTimeout=0)
ser1.write('?\n')
ser1.write('fs1\n')
ser1.write('pd1\n')
ser1.write('dr0\n')
ser1.write('ig8\n')
ser1.write('pg6\n')
ser2 = serial.Serial('COM13', baudrate=9600, writeTimeout=0)
ser2.write('?\n')
ser2.write('fs1\n')
ser2.write('pd1\n')
ser2.write('dr0\n')
ser2.write('ig8\n')
ser2.write('pg6\n')
ser3 = serial.Serial('COM14', baudrate=9600, writeTimeout=0)
ser3.write('?\n')
ser3.write('fs1\n')
ser3.write('pd1\n')
ser3.write('dr0\n')
ser3.write('ig8\n')
ser3.write('pg6\n')

serA = serial.Serial('COM6', baudrate=9600, writeTimeout=0)
serA.write('?\n')

ora_lower = [40,105,165]
ora_higher = [75,140,243]
#ora_lower = [45,115,140]
#ora_higher = [70,140,200]

'''blu_lower = [90,63,0]
blu_higher = [130,93,74]
'''
#yel_lower = [30,155,140]
#yel_higher = [125,190,255]

yel_lower = [50,130,110]
yel_higher = [80,180,155]

'''ora_lower = [0,40,153]
ora_higher = [20,87,233]
'''
blu_lower = [30,40,10]
blu_higher = [50,65,35]
#blu_lower = [30,40,30]
#blu_higher = [60,65,60]
'''yel_lower = [35,129,129]
yel_higher = [71,166,180]'''

bla_lower = [45,70,40]
bla_higher = [65,95,55]
 
whi_lower = [190,240,220]
whi_higher = [255,255,255]

#Yellow goal Red - 234 Green - 205 Blue - 15

#Blue goal Red - 34 Green - 43 Blue - 110

#Ball Red - 193 Green - 55 Blue - 25

cam = cv2.VideoCapture(int(float(sys.argv[1])))   # 0 -> index of camera
cam.set(cv2.cv.CV_CAP_PROP_FPS, 60)
s, img = cam.read()
global koord
global abiK
global look
look = 0

if s:    # frame captured without any errors
    cv2.namedWindow("cam",cv2.CV_WINDOW_AUTOSIZE)
    cv2.moveWindow("cam",25,25)

koord = [(0,0)]

def leia2(image, lower,higher):#leian roboti kontuurjooned, mille jargi saab keskkoha teada
    global koord
    global look
    imgthreshold=cv2.inRange(image,np.uint8(lower),np.uint8(higher))
    contours,hierarchy=cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    b = len(contours)
    pikkus = []
    if (b)!=0:
        for i in range(b):
            a = len(contours[i])
            pikkus.append(a)
	milline = pikkus.index(max(pikkus))#tagastan ainult suurima kontuurpunktide arvuga kujundi#
	x =(np.sum(contours[milline], axis = 0)[0])/len(contours[milline])
	'''while len(contours)>1 and (abs(koord[0][0])-abs(x[0]))>50:
	    del contours[milline]
	    del pikkus[milline]
	    if len(contours)==0:
		break
            milline = pikkus.index(max(pikkus))
            x =(np.sum(contours[milline], axis = 0)[0])/len(contours[milline])'''
	if look==1 and len(contours[milline])<15:
	    return koord
	if look==0:
	    if x[0]>320:
		crop_img = image[x[1]:480,320:x[0]]
		crop_img2 = image[x[1]:480,320:x[0]]
	    else:
                crop_img = image[x[1]:480, x[0]:320]
		crop_img2 = image[x[1]:480, x[0]:320]
	    try:		
                imgthreshold2=cv2.inRange(crop_img.copy(),np.uint8(whi_lower),np.uint8(whi_higher))
		contours2,hierarchy2=cv2.findContours(imgthreshold2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            	b2 = len(contours2)
            	imgthreshold3=cv2.inRange(crop_img2.copy(),np.uint8(bla_lower),np.uint8(bla_higher))
            	contours3,hierarchy3=cv2.findContours(imgthreshold3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            	b3 = len(contours3)
            	if len(max(contours2, key=len)) > 5 and len(max(contours3,key=len)) > 10:
		    koord = [(0,0)]
		    return koord
	    except:
		n = 0
        if look==1 and len(contours[milline])<250:
            if koord[0][0]>320:
                koord=[(640,0)]
            else:
                koord=[(0,0)]
            return koord
        if look==0 and (len(contours[milline])>200 or len(contours[milline])<3):
            if koord[0][0]>320:
                koord=[(640,0)]
            else:
                koord=[(0,0)]
            return koord
	#print len(contours[milline])
	x =(np.sum(contours[milline], axis = 0)[0])/len(contours[milline])
	koord = []
        koord.append(x)	
        return koord
    else:
	if koord[0][0]>320:
	    koord=[(640,0)]
        else:
	    koord=[(0,0)]

def allSpeedsToZero():#Funktsioon paneb koigi rataste kiiruse nulli ja paneb peale automaatse mootorite peatamise.
    ser1.write('wl0\n')
    ser2.write('wl0\n')
    ser3.write('wl0\n')

def allMotorAutomatic():
    ser1.write('fs0\n')
    ser2.write('fs0\n')
    ser3.write('fs0\n')

def drive(threadName, stop_event):
    global koord
    global look
    global joon
    time.sleep(0.5)
    t2 = 0.05
    t4 = 0.03
    t3 = 0
    while(not stop_event.is_set()):
	kiirus2 = 0
	kiirus3 = 0
	if len(koord) == 0:
            print "ei ole"
	    time.sleep(0.0001)
        elif look == 0 and koord[0][1]>int(float(sys.argv[2])) and koord[0][0]>260 and 320>koord[0][0]:
            setSpeed(ser1,ser2,'25','25')
            time.sleep(0.5)
            allSpeedsToZero()
	    continue
        elif look == 1 and (koord[0][0]>560 or (350<koord[0][0] and koord[0][1]>45)):
	    kiirus =min(20, max((koord[0][0]-290)/15,12))
            if look == 1:
                kiirus += 1
            setSpeeds2(ser1,ser2,ser3,str(kiirus))
            time.sleep(t4)
            allSpeedsToZero()
            time.sleep(t3)
            continue
        elif look == 1 and (30>koord[0][0] or (230>koord[0][0] and koord[0][1]>45)):
	    kiirus =min(20, max((290-koord[0][0])/15,12))
            if look == 1:
                kiirus += 1
            setSpeeds(ser1,ser2,ser3,str(kiirus))
            time.sleep(t4)
            allSpeedsToZero()
            time.sleep(t3)
            continue

	elif koord[0][0]>560 or (320<koord[0][0] and koord[0][1]>250):
	    kiirus =min(20, max((koord[0][0]-290)/15,12))
	    if look == 1:
		kiirus += 1
	    setSpeeds2(ser1,ser2,ser3,str(kiirus))
	    time.sleep(t2)
	    allSpeedsToZero()
	    time.sleep(t3)
	    continue
	elif 30>koord[0][0] or (260>koord[0][0] and koord[0][1]>250):
	    kiirus =min(20, max((290-koord[0][0])/15,12))
            if look == 1:
                kiirus += 1
	    setSpeeds(ser1,ser2,ser3,str(kiirus))
            time.sleep(t2)
	    allSpeedsToZero()
	    time.sleep(t3)
	    continue
        #elif koord[0][0]>350 or (320<koord[0][0] and koord[0][1]>220):
            #kiirus3 =min(20, max((koord[0][0]-290)/100,1))
            #setSpeeds2(ser1,ser2,ser3,str(kiirus))
            #time.sleep(t2)
            #allSpeedsToZero()
            #time.sleep(t3)
        #elif 230>koord[0][0] or (260>koord[0][0] and koord[0][1]>220):
            #kiirus2 =-1*min(20, max((290-koord[0][0])/100,1))
            #setSpeeds(ser1,ser2,ser3,str(kiirus))
            #time.sleep(t2)
            #allSpeedsToZero()
            #time.sleep(t3)
        t1=0
	if look == 0:
	    kiirus = max((400-koord[0][1])/5, 40)
	if look == 1:
            kiirus = max((400-koord[0][1])/5, 40)
        setSpeeds3(ser1,ser2,ser3,str(kiirus), str(kiirus2+kiirus3))
        time.sleep(0.1)
	allSpeedsToZero()
	time.sleep(0.001)
	
def setSpeed(ser_1,ser_2, dist1, dist2):
	ser_1.write('sd-'+dist1+'\n')
	ser_2.write('sd'+dist2+'\n')

def setSpeeds(ser_1,ser_2, ser_3, dist1):
        ser_1.write('sd'+dist1+'\n')
	ser_2.write('sd'+dist1+'\n')
	ser_3.write('sd'+dist1+'\n')

def setSpeeds2(ser_1,ser_2, ser_3, dist1):
	ser_1.write('sd-'+dist1+'\n')
        ser_2.write('sd-'+dist1+'\n')
        ser_3.write('sd-'+dist1+'\n')

def setSpeeds3(ser_1,ser_2, ser_3, dist1, dist2):
        ser_1.write('sd-'+dist1+'\n')
        ser_2.write('sd'+dist1+'\n')
        ser_3.write('sd-'+dist2+'\n')


def setSpeedT(ser_3, dist):
	ser_3.write('sd'+dist+'\n')
def lineChecker(threadName, stop_event):
        global look
	global joon
	anb = ""
	while True:
		if serA != None:
		   ef = serA.readline()
		   if ef != None:
		     anb = ef.rstrip()
		if anb == '69':
		   look = 1
		if anb == '96':
		   look = 0
		if anb == '1':
		   joon = int(anb)
		else:
		   joon = 0

global joon
joon = 0
t3_stop= threading.Event()

look_thread = thread.start_new_thread( lineChecker, ("Thread-2", t3_stop))

def find_ball():
    global koord
    global look
    global ser1
    global ser2
    global ser3
    loendur = 0
    palle = 0
    start = datetime.now()
    t1_stop = threading.Event()
    while True:
        if loendur == 2:
	    drive_thread = thread.start_new_thread( drive, ("Thread-1", t1_stop))
        ch = cv2.waitKey(5)
        loendur+=1
        s, img = cam.read()
	if img == None:
	    continue
	img = img[80:480,0:640]
	leia2(img, ora_lower, ora_higher)

        #cv2.circle(img,(koord[0][0], koord[0][1]), 15, (0,0,0), 5)
	#cv2.imshow("cam",img)
	if look==0 and palle != 0:
            palle = 0
            t1_stop.clear()
            drive_thread = thread.start_new_thread( drive, ("Thread-1", t1_stop))
        if look==1:
            palle += 1
	if look==1 and palle>49 :
	    t1_stop.set()
	    time.sleep(0.1)
            allSpeedsToZero()
            koord = [(0,0)]
            loendur = 0
            if sys.argv[3] == "y":
                find_goal(yel_lower, yel_higher)
            else:
                find_goal(blu_lower, blu_higher)
            return

        if ch == 27:
            ch = cv2.waitKey(5)
	    t1_stop.set()
            allSpeedsToZero()
	    allMotorAutomatic()
            sys.exit()
            break	
	
        aeg_kiri = "FPS: "
        end = datetime.now()#fpsi mootmise lopp
        aeg = end-start
        start = datetime.now()#fpsi mootmine alates teisest kaadristx
        l = 1
        fps = str( '%.2f' % (1000000.0/(aeg.microseconds)))
	print(fps)
#	cv2.circle(img,(koord[0][0], koord[0][1]), 15, (255,255,255), 25)#ringjoon keskkoha jaoks
#	cv2.imshow("cam",img)	

def find_goal(c_lower, c_higher):
    global koord
    global look
    global ser1
    global ser2
    global ser3
    koord = [(0,0)]
    number1 = [0,0]
    kiirus_kesk = 0
    loendur = 0
    l = 0
    t2_stop= threading.Event()
    kaader = 0
    while True:
        print look
	if look == 0:
	    t2_stop.set()
            allSpeedsToZero()
            allMotorAutomatic()
            koord = [(0,0)]
            loendur = 0
            find_ball()
            return
	    
        if loendur == 2:
            drive_thread = thread.start_new_thread( drive, ("Thread2", t2_stop))        
        ch = cv2.waitKey(5)
        loendur+=1
        s, img = cam.read()
	if img == None:
	    continue
	img = img[80:480,0:640]
        leia2(img, c_lower, c_higher)
	#cv2.circle(img,(koord[0][0], koord[0][1]), 15, (0,0,0), 5)
	#cv2.imshow("cam",img)
        if koord[0][1]>int(float(45)) and koord[0][0]>240 and koord[0][0]<340:
            print "loo"
	    t2_stop.set()
	    allSpeedsToZero()
	    time.sleep(0.5)
	    print "loo"
	    serA.write('1\n')
	    time.sleep(0.5)
            allSpeedsToZero()
	    koord = [(0,0)]
            loendur = 0
	    find_ball()
	    return

        if ch == 27:
            ch = cv2.waitKey(2)
	    t2_stop.set()
            allSpeedsToZero()
	    allMotorAutomatic()
            sys.exit()
            break

find_ball()    
 
cv2.destroyAllWindows()    
