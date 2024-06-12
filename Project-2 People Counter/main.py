# ACTIVATE CONDA ENVS
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

# Needed
model = YOLO('YOLO-Weight\yolov8n.pt')  # type: ignore
cap = cv2.VideoCapture("Videos\people.mp4")  # type: ignore
tracking = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
mask = cv2.imread("Project-2 People Counter\mask2.png")  # type: ignore
# List of names
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

# LINING COUNTER // LINING SET UP
upwardline = [103, 161, 296, 161]
downline = [527, 489, 735, 489]
totalupwardline = []
totaldownline = []

while True:
    success, img = cap.read()
    masking = cv2.bitwise_and(img, mask)
    imgGraphics = cv2.imread(
        "Project-2 People Counter\graphics.png", cv2.IMREAD_UNCHANGED)  # type: ignore
    img = cvzone.overlayPNG(img, imgGraphics, (730, 260))
    results = model(masking, stream=True)
    detections = np.empty((0, 5))
    # For Rectangle
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2-x1, y2-y1
            # Confidence level
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class name
            cls = int(box.cls[0])
            # change into str not an int (if 0 = person)
            nameClass = classNames[cls]
            if nameClass == "person" and conf > 0.3:
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))
                # cvzone.cornerRect(img, (x1, y1, w, h), l=3)
    trackingResult = tracking.update(detections)
    # Lining
    cv2.line(img, (upwardline[0], upwardline[1]),
             (upwardline[2], upwardline[3]), (0, 0, 255), 5)
    cv2.line(img, (downline[0], downline[1]),
             (downline[2], downline[3]), (0, 0, 255), 5)

    # Tracking
    for result in trackingResult:
        x1, y1, x2, y2, ID = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(result)
        w, h = x2-x1, y2-y1
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
        # DOT / circle in the tracker
        cx, cy = x1+w//2, y1+h//2
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        # For showing id on top of tracker
        cvzone.putTextRect(img, f'{int(ID)}', (max(0, x1), max(35, y1)))
        # Set up center line for counting
        if upwardline[0] < cx < upwardline[2] and upwardline[1] - 15 < cy < upwardline[1] + 15:
            if totalupwardline.count(ID) == 0:
                totalupwardline.append(ID)
                cv2.line(img, (upwardline[0], upwardline[1]),
                         (upwardline[2], upwardline[3]), (255, 0, 0), 5)
        if downline[0] < cx < downline[2] and downline[1] - 15 < cy < downline[1] + 15:
            if totaldownline.count(ID) == 0:
                totaldownline.append(ID)
                cv2.line(img, (downline[0], downline[1]),
                         (downline[2], downline[3]), (255, 0, 0), 5)
    # Adding graphics
    cv2.putText(img, f'{len(totalupwardline)}', (929, 345),
                cv2.FONT_HERSHEY_PLAIN, 5, (139, 195, 75), 7)
    cv2.putText(img, f'{len(totaldownline)}', (1191, 345),
                cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 230), 7)
    # Showing Img
    cv2.imshow("People", img)
    # cv2.imshow("region", masking)
    cv2.waitKey(1)
