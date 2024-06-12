# You must first activate the conda env
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *


cap = cv2.VideoCapture("Videos\cars.mp4") # note : for reach out the videos you need to use relative path \\ # type: ignore
mask = cv2.imread("Project-1 Car Counter\mask.png") # type: ignore
model = YOLO('YOLO-Weight\yolov8n.pt') # type: ignore

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# Tracking
tracking = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
# Line 
limits = [400,297,673,297]
totalCount = []
while True :
    success, img = cap.read()
    region = cv2.bitwise_and(img,mask)
    results = model(region, stream=True)
    detections = np.empty ((0,5))
    for r in results :
        boxes = r.boxes
        # bounding box
        for box in boxes :
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
            w, h = x2-x1, y2-y1
            # cvzone.cornerRect(img, (x1,y1,w,h), l=9,)
            # confidence level
            conf = math.ceil((box.conf[0] * 100 )) / 100
            # class name
            cls = int(box.cls[0])
            classCounter = classNames[cls]
            if classCounter == "car" or classCounter == "motorbike"\
                or classCounter == "bus" or classCounter=="truck" or classCounter=="person"\
                and conf > 0.3 :
                # cvzone.putTextRect(img, f'{classCounter} {conf}', (max(0,x1), max(35,y1)), scale =0.6 , # type: ignore
                #                     thickness=1, offset =3)
                # cvzone.cornerRect(img, (x1,y1,w,h), l=9, rt=5)
                currentArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections, currentArray))

    trackingResults = tracking.update(detections) # type: ignore
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0,0,255), 5)

    for result in trackingResults :
        x1,y1,x2,y2,ID = result
        x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
        print(result)
        w, h = x2-x1, y2-y1
        cvzone.cornerRect(img, (x1,y1,w,h), l=9, rt=2, colorR =(255,0,0))
        cvzone.putTextRect(img, f'{int(ID)}', (max(0,x1), max(35,y1)), scale =3 ,# type: ignore
                            thickness=2, offset =3)

        cx,cy = x1+w//2, y1+h//2
        cv2.circle(img,(cx,cy), 5, (255,0,255), cv2.FILLED)

        if limits[0] <cx< limits[2] and limits[1]-20 <cy< limits[1]+10 :
            if totalCount.count(ID) == 0 :
                totalCount.append(ID)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (255,0,0), 5)
    cvzone.putTextRect(img, f'Count :{len(totalCount)}', (20, 50))

    cv2.imshow('Image', img)
    cv2.waitKey(1)