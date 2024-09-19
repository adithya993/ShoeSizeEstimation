import cv2.cv as cv
import cv2
import numpy as np
cap = cv2.VideoCapture(0)
men_size=0
women_size=0
diam=1
#ctr = 0
#sum_len = 0
tmr = 0      ##variable counter
lens = []    ##holds all the lengths that are scanned
dias = []    ##holds all the diameters that are scanned
centi=[]     ##holds all the centimeters estimated from length and diameter
while tmr<500:
    ret,im = cap.read()
    cv2.rectangle(im,(200,200),(600,400),(255,255,255))
    img = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    cv2.imshow("INPUT",im)
    
    if cv2.waitKey(10) == 27:
        cv2.destroyAllWindows()
        break
            
    
    try:
        circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT,1,100,param1=100,param2=50,minRadius = 0, maxRadius = 0)
        try:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(im,(i[0],i[1]),i[2],(0,255,0),2)
                cv2.circle(im,(i[0],i[1]),2,(0,0,255),3)
            diam = i[2] * 2.0
            dias.append(diam)
            cv2.putText(im, "Diameter:: "+str(diam),(i[0]-20,i[1]+20),cv2.FONT_HERSHEY_SIMPLEX,1,0)
        except IndexError:
            print("IE") 
            pass
    except AttributeError:
        pass
    img = img[200:400,200:600]
    thresh22 = cv2.threshold(img, 180, 127, cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
    thresh22 = thresh22[1]
    adapthresh = cv2.adaptiveThreshold(thresh22,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    ##cv2.imshow("adaptive",adapthresh)
    median=cv2.medianBlur(adapthresh,5)
    ##cv2.imshow("medianblur",median)
    thresh = cv2.threshold(adapthresh, 180, 127, cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
    thresh = thresh[1]

##    thresh = cv2.GaussianBlur(thresh,(11,11),0)
    flag = 0
    for j in range(400):
        for i in range(200):
            if thresh[i][j] == 127:
                #cv2.line(im, (j+200,i),(j+200,480),(255,255,0))
                cv2.line(thresh, (j,i),(j,480),(255,255,0))
                flag = 1
#                l1 = j
                (x1,y1)=(j,i)
                break
        if flag == 1:
            break
##    print l1
    for j in range(399,0,-1):
        for i in range(200):
            if thresh[i][j] == 127:
                cv2.line(thresh, (j,i),(j,480),(255,255,255))
                
                flag = 0
##                l2 = j
                (x2,y2)=(j,i)
                break
        if flag == 0:
            break
    
    length = (x2-x1)+(y2-y1)
    lens.append(length)
    cv2.imshow("TRESH",thresh)
    cv2.putText(im, str(length), (x1+50,i+30),cv2.FONT_HERSHEY_SIMPLEX,1,0)

    #image calibration
    scale=2.5/diam
    actual_length_incenti=scale*length
    centi.append(actual_length_incenti)
    cv2.imshow("OUTPUT",im)

    if cv2.waitKey(10) == 99:
        cv2.imwrite("frame"+str(ctr)+".jpg",im)
        ctr+=1

        
    tmr+=1
cv2.destroyAllWindows()
#counter over
    

actual_length_incenti=np.mean(centi)

actual_length=actual_length_incenti*10

if actual_length>226 and actual_length<230: #'228'
    men_size=3
    women_size=3
if actual_length>229 and actual_length<233: #'231'
    men_size=4
    women_size=3
if actual_length>233 and actual_length<237: #'235'
    men_size=4
    women_size=4
if actual_length>236 and actual_length<240: #'238'
    men_size=5
    women_size=4
if actual_length>239 and actual_length<243: #'241'
    men_size=5
    women_size=5
if actual_length>243 and actual_length<247: #'245'
    men_size=6
    women_size=5
if actual_length>246 and actual_length<250: #'248'
    men_size=6
    women_size=6
if actual_length>249 and actual_length<253: #'251'
    men_size=7
    women_size=6
if actual_length>252 and actual_length<256: #'254'
    men_size=7
    women_size=7
if actual_length>255 and actual_length<259: #'257'
    men_size=8
    women_size=7
if actual_length>258 and actual_length<262: #'260'
    men_size=8
    women_size=8
if actual_length>265 and actual_length<269: #'267'
    men_size=9
    women_size=9
if actual_length>271 and actual_length<275: #'273'
    men_size=10
    women_size=10
if actual_length>277 and actual_length<281: #'279'
    men_size=11
    women_size=11
if actual_length>284 and actual_length<288: #'286'
    men_size=12
    women_size=11
if actual_length>290 and actual_length<294: #'292'
    men_size=13
    women_size=12
else:
    print('couldnt capture. please try again')
    
print(actual_length_incenti,' cm') 
print(men_size) 
print(women_size) 

