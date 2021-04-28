import cv2
import os
import time
import module as htm

def most_frequent(List):
    counter = 0
    num = List[0]
      
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
  
    return num

cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

folderPath = 'img'
myList = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']

overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipId = [4,8,12,16,20]
capture = True

frame = 0
ress = []
limit = 20 #duration to capture the frame
while capture:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = []

        #untuk jempol
        if lmList[tipId[0]][1] < lmList[tipId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)        

        #4 jari yg lain
        for id_s in range(1,5):
            if lmList[tipId[id_s]][2] < lmList[tipId[id_s]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)        

        totalFingers = fingers.count(1)
        ress.append(totalFingers)
    
        h,w,c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]
        frame += 1
        
        if frame == limit:
            break


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img, f'FPS: {int(fps)}', (1000,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
print("Deteksi : ",most_frequent(ress))
