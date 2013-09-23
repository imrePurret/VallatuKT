<<<<<<< HEAD
def nurgad(img, img2, varv_r_b, varv_r_g, varv_r_r, r_dev_b, r_dev_g, r_dev_r, varv_s_b, varv_s_g, varv_s_r, s_dev_b, s_dev_g, s_dev_r ):
    import numpy as np
    import cv2
    import math
    import sys
    import colorsys
    from time import sleep
=======
import numpy as np
import cv2
import math
import sys
import colorsys

def nurk(img, img2, varv_r_b,varv_r_g,varv_r_r, r_dev_b,r_dev_g,r_dev_r, s_dev_b,s_dev_g,s_dev_r ):
>>>>>>> 42fa8549fdd7cfb30c8e04ca85d2bd65ffabe02e
    def leia(image, lower, higher):#leiab ules kujundid
        global koord
        imgthreshold=cv2.inRange(image.copy(),np.uint8(lower),np.uint8(higher))
        #cv2.imshow("cam-test",imgthreshold)
        contours,hierarchy=cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        b = len(contours)
        koord = []
        #print len(contours)
        for i in range(b):
            x =(np.sum(contours[i], axis = 0)[0])/len(contours[i])
            if len(contours[i])> 80:
                koord.append(x)

        return koord

    def nega(a):#et mu deviations list ei laheks negatiivseks ega ule lubatud piiride
        for i in range(3):
<<<<<<< HEAD
            if a[i]<=0:
                a[i]=0
        for i in range(3):
            if a[i]>=255:
=======
            if a[i]<0:
                a[i]=0
        for i in range(3):
            if a[i]>255:
>>>>>>> 42fa8549fdd7cfb30c8e04ca85d2bd65ffabe02e
                a[i]=255
        return a        
    def A(dx, dy):#arvutab nurga
      return (math.atan2(dy, dx))* 180 / math.pi

    #image=cv2.imread('sample08.tiff')
    global koord
    '''
    img = cv2.imread(sys.argv[1])
    img2 = cv2.imread(sys.argv[2])
    varv_r_b = int(float(sys.argv[3]))
    varv_r_g = int(float(sys.argv[4]))
    varv_r_r = int(float(sys.argv[5]))
    r_dev_b = int(float(sys.argv[6]))
    r_dev_g = int(float(sys.argv[7]))
    r_dev_r = int(float(sys.argv[8]))
    varv_s_b = int(float(sys.argv[9]))
    varv_s_g = int(float(sys.argv[10]))
    varv_s_r = int(float(sys.argv[11]))
    s_dev_b = int(float(sys.argv[12]))
    s_dev_g = int(float(sys.argv[13]))
    s_dev_r = int(float(sys.argv[14]))
    '''
    lower = []
    higher = []
    lower3 = []
    higher4 = []
    lower.append(varv_s_b-s_dev_b), lower.append(varv_s_g-s_dev_g), lower.append(varv_s_r-s_dev_r)
    higher.append(varv_s_b+s_dev_b), higher.append(varv_s_g+s_dev_g), higher.append(varv_s_r+s_dev_r)
    lower3.append(varv_r_b- r_dev_b), lower3.append(varv_r_g- r_dev_g), lower3.append(varv_r_r- r_dev_r)
    higher4.append(varv_r_b+r_dev_b), higher4.append(varv_r_g+r_dev_g), higher4.append(varv_r_r+r_dev_r)
<<<<<<< HEAD
=======

>>>>>>> 42fa8549fdd7cfb30c8e04ca85d2bd65ffabe02e
    lower = nega(lower)
    higher = nega(higher)
    lower3 = nega(lower3)
    higher4 = nega(higher4)
    b=leia(img2, lower, higher)
    c=leia(img, lower3, higher4)
    nega(lower), nega (higher), nega(lower3), nega(higher4)
    d=leia(img2, lower3, higher4)
<<<<<<< HEAD
    cv2.namedWindow("cam-test",cv2.CV_WINDOW_AUTOSIZE)
    cv2.line(img, c, d, (255,155,155), 3, 8)
    cv2.imshow("cam-test",img)
    print "tere"

    if len(c) and len(d) !=0 and len(b) and len(d) !=0:
=======

    if ((len(c) and len(d) !=0) and len(b) !=0):
>>>>>>> 42fa8549fdd7cfb30c8e04ca85d2bd65ffabe02e
        esimene =  A((d[0][0])-(c[0][0]), (d[0][1])-(c[0][1]))

        teine =  A((b[0][0])-(d[0][0]),(b[0][1])-(d[0][1]))
    else:
        print "Probleem objekti tuvastusega"
    esimene = esimene*-1
    teine = teine*-1
    #print math.fabs(esimene)-math.fabs(teine)

    if b[0][0]> d[0][0] and b[0][1]< d[0][1] and c[0][1]>d[0][1]:
<<<<<<< HEAD
        return (c,d,b,(math.fabs(esimene)-math.fabs(teine))*-1)

    else:
        return (c,d,b, (math.fabs(math.fabs(esimene)-math.fabs(teine))))






=======
        print (math.fabs(esimene)-math.fabs(teine))*-1

    else:
        print math.fabs(math.fabs(esimene)-math.fabs(teine))
>>>>>>> 42fa8549fdd7cfb30c8e04ca85d2bd65ffabe02e
     



