# forwarder.py
# โปรแกรมนี้เป็น node ตัวกลาง ที่รับข้อความจาก pub.py (msg1) แล้วเปลี่ยน Topic เป็น msg2
# จากนั้นก็เผยแพร่ใหม่อีกครั้ง ให้ sub.py มารับที่Topic msg2

import zmq

# สร้าง context สำหรับ socket
context = zmq.Context()

# ---------- ส่วน Subscriber ----------
# สร้าง socket แบบ SUB เพื่อรับข้อมูลจาก pub.py
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5555")  # เชื่อมต่อกับ Publisher ที่พอร์ต 5555
subscriber.setsockopt_string(zmq.SUBSCRIBE, "msg1")  # ติดตามเฉพาะข้อความที่มี Topic msg1

# ---------- ส่วน Publisher ----------
# สร้าง socket แบบ PUB เพื่อส่งข้อมูลต่อไปยัง sub.py
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")  # bind พอร์ตใหม่สำหรับเผยแพร่ข้อความต่อไป

while True:
    # รอรับข้อความที่ Topic msg1 จากต้นทาง
    received = subscriber.recv_string()  # ตัวอย่าง: "msg1 Hello from original publisher"

    # แยกข้อความออกเป็น topic และเนื้อหา
    topic, content = received.split(' ', 1)

    # เปลี่ยน Topic เป็น msg2 ก่อนส่งออกใหม่
    new_topic = "msg2"
    new_message = f"{new_topic} {content}"

    print("🔁 ส่งต่อ:", new_message)
    publisher.send_string(new_message)
