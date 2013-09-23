import cv2
import math
import sys
import colorsys
import numpy as np
from time import sleep


def leia(image, lower, higher):#leiab ules kujundid
    global koord
    global koordinaadid
    global contours
    global b
    koordinaadid = []
    imgthreshold=cv2.inRange(image.copy(),np.uint8(lower),np.uint8(higher))
    #cv2.imshow("cam-test",imgthreshold)
    contours,hierarchy=cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    b = len(contours)
    koord = []
    #print len(contours)
    for i in range(b):
        x =(np.sum(contours[i], axis = 0)[0])/len(contours[i])
        if len(contours[i])> 20:
            koord.append(x)
        
    return koord, contours

    
     
    
def punkt_kaugus(img, a1,a2,b1,b2):#eimene funkt, mis leiab kahe punkti vahelise kauguse
    if (a1 <= len(img) and (a1 >=0))and (a2 <= len(img[0]) and (a2 >= 0)):
        #print math.sqrt((a1-b1)**2 +(a2-b2)**2)
        return math.sqrt((a1-b1)**2 +(a2-b2)**2)
    else:
        return 9999
def punkt_kaugus2(img, a1,a2,b1,b2):
    if (a1 <= len(img) and (a1 >=0))and (a2 <= len(img[0]) and (a2 >= 0)):
        #print math.sqrt((a1-b1)**2 +(a2-b2)**2)
        return math.sqrt((a1-b1)**2 +(a2-b2)**2)
    else:
        return None
    

def min_kaugus(img, x, y, x_l, y_l):#funktsioon, mis leiab kaheksaruudustikus ruudu, mille kaugus loppu on minimaalne
    
    ules = punkt_kaugus(img, x, y-1, x_l, y_l)
    alla = punkt_kaugus(img, x, y+1, x_l, y_l)
    paremale = punkt_kaugus(img, x+1, y, x_l, y_l)
    vasakule = punkt_kaugus(img, x-1, y, x_l, y_l)
    u_par = punkt_kaugus(img, x+1, y-1, x_l, y_l)
    u_vas = punkt_kaugus(img, x-1, y-1, x_l, y_l)
    a_par = punkt_kaugus(img, x+1, y+1, x_l, y_l)
    a_vas = punkt_kaugus(img, x-1, y+1, x_l, y_l)
    miinimum = min(ules,alla,paremale,vasakule,u_par,u_vas,a_par,a_vas)
    if miinimum == ules :
        return [x,y-1]
    if miinimum == alla :
        return [x,y+1]
    if miinimum == paremale :
        return [x+1,y]
    if miinimum == vasakule :
        return [x-1,y]
    if miinimum == u_par :
        return [x+1,y-1]
    if miinimum == u_vas :
        return [x-1,y-1]
    if miinimum == a_par :
        return [x+1,y+1]
    if miinimum == a_vas :
        return [x-1,y+1]
    
def umber_kujundi(img, mil, x1, y2, kujund):#otsib tee umber kujundi, kust saab labi jne
    
    kaugused = []
    for i in range(len(kujund[mil])):
        
        x,y = kujund[mil][i]
        
        kaugused.append(punkt_kaugus2(img,x,y,x1 ,y2))
    miiinimu1 = kaugused.index(min(kaugused))
    
    ab = kujund[mil][miiinimu1]
    
    #print kaugused
    a =kujund[mil][miiinimu1]
    kujund[mil].remove(a)
    
    return ab, kujund
    
        

       
img = cv2.imread(sys.argv[1])

x = []
bbb = []
img = cv2.imread(sys.argv[1])
algus_rida = int(float(sys.argv[2]))
algus_veerg = int(float(sys.argv[3]))
l_rida =varv_b = int(float(sys.argv[4]))
l_veerg = varv_b = int(float(sys.argv[5]))
r_raadius = varv_b = int(float(sys.argv[6]))
x = [algus_rida,algus_veerg]
l_punkt = [l_rida,l_veerg]

a, punktid = leia(img, [245,245,245],[255,255,255])


kujund = []

for i in range(len(punktid)):#joonistan bounding recatngle umber kujundi, et saada takistuse punktid
    kujund.append(cv2.boundingRect(np.array(punktid[i])))
kujund = list(kujund)
 
for i in range(len(kujund)):#lisan eelmistele punktidele juurde roboti radiuse
    kujund[i]=list(kujund[i])
    for j in range(len(kujund[i])):
        if j <= 1:
            kujund[i][j] = kujund[i][j] -r_raadius
        else:
            kujund[i][j] = r_raadius + kujund[i][j]
            
kujundite_punktid = []
for i in range(len(kujund)):#teen eraldi listi takistuse nelja punkti jaoks, kus on juba juurde liidetud a roboti raadius
    a=[kujund[i][0],kujund[i][1]]
    b=[kujund[i][0]+kujund[i][2],kujund[i][1]]
    c = [kujund[i][0],kujund[i][1]+kujund[i][3]]
    d = [kujund[i][0]+kujund[i][2],kujund[i][1]+kujund[i][3]]
    l = [a,b,c,d]
    kujundite_punktid.append(l)
tt = True
mil_kujund = 0
if np.alltrue(img[x[0]][x[1]] == [255,255,255]):
    print "alustasid kujundi seest"
    tt = False

while tt:
    
    if np.alltrue(x == l_punkt):
        bbb.append(x)
        tt = False
        break
    
    x = min_kaugus(img,x[0],x[1],l_punkt[0],l_punkt[1])  
    if np.alltrue(img[x[0]][x[1]] == [255,255,255]):#otsib teed ja kontrollib ega pole sattunud valgele ruudule
        
        for i in range(len(punktid)):
            for j in range(len(punktid[i])):
                if np.alltrue(punktid[i][j] == [x[1],x[0]]):#otsib ules millise takistusega on tegemist, et saata see umber_kujundi funktsioonile
                
                   
                    mil_kujund = i
                    
                    
                    oige_koht,uus_punkt = umber_kujundi(img,mil_kujund,x[1],x[0], kujundite_punktid)
                    
                    if (oige_koht[0] >= len(img) or (oige_koht[0] <=0))or (oige_koht[1] >= len(img[0]) or (oige_koht[1] <= 0)):#kui pole teed, terve pilt on kujundit tais
                        print "Teed pole"
                        tt = False
                        break
                    x[0] = oige_koht[1]
                    x[1] = oige_koht[0]
                    bbb.append(x)
                    kujundite_punktid = uus_punkt
                
        


print  bbb[0]

