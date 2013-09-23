# -*- coding: cp1257 -*-
#Martin Molder pikslisuhte leidmine
import math
import sys
import cv2
import colorsys
import numpy as np
from time import sleep

def leia(image, lower, higher):#leiab ules kujundidite kontuurid
        global koord
        global kontuur
        imgthreshold=cv2.inRange(image.copy(),np.uint8(lower),np.uint8(higher))
        #cv2.imshow("cam-test",imgthreshold)
        contours,hierarchy=cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        b = len(contours)
        koord = []
        kontuur = []
        for i in range(b):#teen listi kõikidest kontuuri koordinaatidest, kui kontuuri
            #pikkus alla 80 piksli, siis ei võta seda arvesse(mura)
            if len(contours[i]) >= 80:
                kontuur.append(contours[i])
        
        #print len(contours)
        for i in range(b):#leian keskkoha koordinaadid, samuti ei arvesta alla 80piksli pikkust
            #kontuuri, see ka mura
            x =(np.sum(contours[i], axis = 0)[0])/len(contours[i])
            if len(contours[i])> 80:
                koord.append(x)

        return koord , kontuur

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
    
img = cv2.imread(sys.argv[1])
varv_b = int(float(sys.argv[2]))
varv_g = int(float(sys.argv[3]))
varv_r = int(float(sys.argv[4]))
r_dev_b = int(float(sys.argv[5]))
r_dev_g = int(float(sys.argv[6]))
r_dev_r = int(float(sys.argv[7]))
suurus = int(float(sys.argv[8]))
lower = []
higher= []
lower.append(varv_b-r_dev_b), lower.append(varv_g-r_dev_g), lower.append(varv_r-r_dev_r)
higher.append(varv_b+r_dev_b), higher.append(varv_g+r_dev_g), higher.append(varv_r+r_dev_r)
lower = nega(lower)
higher = nega(higher)
a = leia(img, lower,higher)
kaugus11 = 0#kaugused vordlemiseks 
kaugus22 = 0
kaugus33 = 0
kaugus_u_v = []
kaugus_u_p = []
kaugus_a_v = []
for i in range(len(kontuur[0])):#leian kujundi koige ulemise vasaku ja  ulemise parema piksli
    #ja alumise vasaku piksli, et leida pikim kulg
    a = kontuur[0][i]
    if (a[0][0] < koord[0][0] and a[0][1]  < koord[0][1]) :#ulemine vasak
        kaugus1 = punkt_kaugus(a[0][0],a[0][1],koord[0][0],koord[0][1])
        if kaugus1 > kaugus11:
            kaugus_u_v = a
            kaugus11 = kaugus1
    if (a[0][0] > koord[0][0] and a[0][1]  < koord[0][1]) :#ulemine parem
        kaugus2 = punkt_kaugus(a[0][0],a[0][1],koord[0][0],koord[0][1])
        if kaugus2 > kaugus22:
            kaugus_u_p = a
            kaugus22 = kaugus2
    if (a[0][0] < koord[0][0] and a[0][1]  > koord[0][1]) :#alumine vasak
        kaugus3 = punkt_kaugus(a[0][0],a[0][1],koord[0][0],koord[0][1])
        if kaugus3 > kaugus33:
            kaugus_a_v = a
            kaugus33 = kaugus3

esimene = punkt_kaugus(kaugus_u_v[0][0],kaugus_u_v[0][1],kaugus_u_p[0][0],kaugus_u_p[0][1])#horisontaalne kulg
teine =  punkt_kaugus(kaugus_u_v[0][0],kaugus_u_v[0][1],kaugus_a_v[0][0],kaugus_a_v[0][1])#vertikaalne kulg
kordaja = 1000.0/suurus#et saaks pikslite oige suuruse
print round((max(esimene, teine)+1)*kordaja)




