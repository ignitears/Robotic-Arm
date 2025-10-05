# sub.py
# โปรแกรมนี้จะทำหน้าที่เป็น Subscriber รับข้อความที่ถูกส่งต่อมาจาก forwarder.py ในหัวข้อ msg2

import zmq

# สร้าง context สำหรับ socket
context = zmq.Context()

# ---------- ส่วน Subscriber ----------
# สร้าง socket แบบ SUB เพื่อรับข้อมูลจาก forwarder.py
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5556")  # เชื่อมต่อกับ forwarder.py ที่พอร์ต 5556
subscriber.setsockopt_string(zmq.SUBSCRIBE, "msg2")  # ติดตามเฉพาะข้อความที่มีหัวข้อ msg2

print("📥 รอฟังข้อความจากหัวข้อ 'msg2'...")

while True:
    # รับข้อความจาก forwarder.py
    message = subscriber.recv_string()  # ตัวอย่าง: "msg2 Hello from original publisher"

    # แยกหัวข้อออกจากเนื้อหา
    topic, content = message.split(' ', 1)
    print(f"📨 ได้รับข้อความ: {content}")
