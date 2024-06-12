from ultralytics import YOLO
import cv2
import cvzone
import math

capture = cv2.VideoCapture("C:\\Users\\Wellson\\Documents\\ObjectDetection\\Videos\\ppe-2.mp4")

model = YOLO("C:\\Users\\Wellson\\Documents\\ObjectDetection\\Project-3 PPE Detection\\ppe.pt") # type: ignore

className = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
            'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

defaultColor = (0, 0, 255)

while True:
    success, img = capture.read()
    
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = math.ceil((box.conf[0]*100)) / 100
            cls = int(box.cls[0])
            Class = className[cls]
            
            if conf > 0.5:
                if Class == 'NO-Hardhat' or Class == 'NO-Mask' or Class == 'NO-Safety Vest':
                    defaultColor = (0, 0, 255)
                elif Class == "Hardhat" or Class == "Mask" or Class == "Safety Vest":
                    defaultColor = (0, 255, 0)
                else:
                    defaultColor = (0, 0, 0)
                    
                cv2.rectangle(img, (x1, y1), (x2, y2), defaultColor, 2)
                
                cvzone.putTextRect(img, f'{className[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1, colorT=(255, 255, 255), colorR=(defaultColor), colorB=(defaultColor))
                
    cv2.imshow("PPE", img)
    cv2.waitKey(1)