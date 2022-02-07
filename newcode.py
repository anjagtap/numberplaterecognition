import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cascade=cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
states={"AN":"Andaman","MH":"MAHARASHTRA","DL":"DELHI","KA":"KARNATAKA","HP":"HIMACHAL PRADESH",
        "GJ":"GUJARAT","RJ":"RAJASTHAN","AP":"ANDHRA PRADESH","UP":"UTTAR PRADESH"}

def extract_num(img_name):
    global read
    img=cv2.imread(img_name)
    #converting image to gray
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    nplate=cascade.detectMultiScale(gray,1.3,6)
    #crop the number plate:
    for (x,y,w,h) in nplate:
        a,b=(int(0.02*img.shape[0]),int(0.025*img.shape[1]))
        plate=img[y+a:y+h-a,x+b:x+w-b,:]
        cv2.imshow('Plate', plate)
        kernel=np.ones((1,1),np.uint8)
        plate=cv2.dilate(plate,kernel,iterations=1)
        plate=cv2.erode(plate,kernel,iterations=1)
        plate_gray=cv2.cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
        (thresh,plate)=cv2.threshold(plate_gray,127,255,cv2.THRESH_BINARY)

        read=pytesseract.image_to_string(plate)
        read=''.join(e for e in read if e.isalnum())
        stat=read[0:2]
        print(stat)
        try:
            print('Car belongs to ',states[stat],' state.')
        except:
            print('State not recognised!!')
        print(read)
        cv2.rectangle(img,(x,y),(x+w+40,y+h),(51,51,255),2)
        cv2.rectangle(img,(x,y-40),(x+w+40,y),(51,51,255),-1)
        cv2.putText(img, read, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
        cv2.imshow('Plate',plate)

    cv2.imshow("Result",img)
    # if cv2.waitKey(0)==113:
    #     exit()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

extract_num('.\images\skodarapid.jpg')
# extract_num('.\images\SKODA.jpg')
# extract_num('.\images\Wbackpolo.jpg')
# extract_num('.\images\Tnexon.jpg')
# extract_num('.\images\Ttata.jpg')
# extract_num('.\images\BMW.jpg')
# extract_num('.\images\Ffortuner.jpg')
# extract_num('.\images\swift.jpg')



