import numpy as np
import cv2
import colorsys
from time import sleep
import math
import sys
import timeit
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
        for i in range(b):
            a = len(contours[i])
            pikkus.append(a)
        milline = pikkus.index(max(pikkus))#tagastan ainult suurima kontuurpunktide arvuga kujundi
        x =(np.sum(contours[milline], axis = 0)[0])/len(contours[milline])
        koord.append(x)
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

varv_b = int(float(sys.argv[1]))
varv_g = int(float(sys.argv[2]))
varv_r = int(float(sys.argv[3]))
r_dev_b = int(float(sys.argv[4]))
r_dev_g = int(float(sys.argv[5]))
r_dev_r = int(float(sys.argv[6]))

lower = []
higher= []

lower.append(varv_b-r_dev_b), lower.append(varv_g-r_dev_g), lower.append(varv_r-r_dev_r)
higher.append(varv_b+r_dev_b), higher.append(varv_g+r_dev_g), higher.append(varv_r+r_dev_r)

lower = nega(lower)
higher = nega(higher)

cam = cv2.VideoCapture(int(sys.argv[7]))   # 0 -> index of camera
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
    cv2.circle(img,(koord[0][0], koord[0][1]), 10, (0,0,255), 5)#ringjoon keskkoha jaoks
    cv2.circle(img,(koord[0][0], koord[0][1]), 5, (0,255,0), 5)

    kiri = "Koordinaat: "
    number = [koord[0][1],koord[0][0]]#siit edasi tulevad tesktid, mida kuvada
    tekst2 = str(number)
    kolmas = str(kiri+tekst2)
    koordiabi = tekst2
    
    frame = str(loendur)
    frame_kiri = "Frame: "
    frame_kokku = str(frame_kiri+frame)
    
    speed_kiri = "Kiirus: "
    kiirus = str('%.2f' % (punkt_kaugus(number[0],number[1],number1[0],number1[1])))
    kiirus_kokku = str(speed_kiri+kiirus)
    kiirus_int = punkt_kaugus(number[0],number[1],number1[0],number1[1])
    
    if loendur > 5: #mootma hakkab viiendast sekundist keskmist, siis ei lahe alguse mootmisvead sisse
        kiirus_kesk = (kiirus_kesk*(loendur-1)+kiirus_int)/loendur
        kiirus_kesk_str = str('%.2f' % ((kiirus_kesk*loendur+kiirus_int)/loendur))#arvutan keskmise, ule koikide kaadrite
        kiirus_kesk_kiri = "Keskmine kiirus: "
        kiirus_kesk_kokku =str(kiirus_kesk_kiri+kiirus_kesk_str)
        
    cv2.putText(img,kolmas , (5,15), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#koordinaadid
    
    cv2.putText(img,frame_kokku , (5,30), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#frame
    
    cv2.putText(img,kiirus_kokku , (5,45), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#kiirus
    
    if loendur > 10:#naitan keskmist alles peale 10 kaadrir, siis saan juba oige numbri
        cv2.putText(img,kiirus_kesk_kokku , (5,60), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)
        
    aeg_kiri = "FPS: "       
    end = datetime.now()#fpsi mootmise lopp
    aeg = end-start
    start = datetime.now()#fpsi mootmine alates teisest kaadrist
    l = 1
    fps = str( '%.2f' % (1000000.0/(aeg.microseconds)))
    aeg_kokku =str(aeg_kiri+fps)
    
    cv2.putText(img,aeg_kokku , (5,75), cv2.FONT_HERSHEY_PLAIN, 1.0, [255,0,0], 1)#fps ekraanile
    
    cv2.imshow("cam-test",img)
    number1 = number
    
    if ch == 27:
        ch = cv2.waitKey(5)
        break
    
cv2.destroyAllWindows()

