# node1.py
# ตรวจจับ "board_shield" ด้วย YOLOv8 และส่งค่า center-X ผ่าน ZMQ (JSON)

import cv2
import zmq
import json
import time
from ultralytics import YOLO

# ─────────────────── 1) โหลดโมเดล YOLO ───────────────────
model = YOLO("best.pt")  # ไฟล์โมเดล custom
CONFIDENCE_THRESHOLD = 0.25
TARGET_CLASS = "donut_green"

# ─────────────────── 2) เปิดกล้อง ───────────────────
cap = cv2.VideoCapture(1)  # 0 = กล้องหลัก, 1 = USB cam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

# ─────────────────── 3) สร้าง ZMQ Publisher ───────────────────
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5555")
print("📡 Publisher เริ่มที่ tcp://*:5555 topic 'board_shield'")
time.sleep(1)  # รอให้ subscriber เชื่อมต่อ

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ ไม่สามารถอ่านภาพจากกล้องได้")
        break

    results = model(frame)[0]
    center_x = None

    for box in results.boxes:
        conf = float(box.conf)
        if conf < CONFIDENCE_THRESHOLD:
            continue

        cls_id = int(box.cls[0])
        label = model.names[cls_id]

#        if label != TARGET_CLASS:
 #           continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        center_x = int((x1 + x2) / 2)

        # วาดกรอบและ label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f"{label} {conf:.2f}"
        cv2.putText(frame, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.circle(frame, (center_x, int((y1 + y2) / 2)), 5, (0, 0, 255), -1)

        break  # เอาเฉพาะกล่องแรก

    # ✅ Always publish
    if center_x is not None:
        data = {"x": center_x, "name": TARGET_CLASS}
    else:
        data = {"x": -1, "name": None}

    json_message = json.dumps(data)
    full_message = f"board_shield {json_message}"
    publisher.send_string(full_message)
    print("📤 ส่ง:", full_message)

    cv2.imshow("YOLOv8 board_shield Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
publisher.close()
context.term()
