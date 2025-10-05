# pub.py
# โปรแกรมนี้เป็นตัวเผยแพร่ข้อมูล (Publisher) โดยใช้ ZeroMQ PUB socket
# มันจะส่งข้อความพร้อมกับ "topic" ไปยังผู้ติดตาม (Subscriber) ทุกตัวที่ subscribe topic เดียวกัน

import zmq
import time

# สร้าง context สำหรับ ZeroMQ ซึ่งเป็นสิ่งจำเป็นสำหรับ socket ทั้งหมด
context = zmq.Context()

# สร้าง socket แบบ PUB สำหรับเผยแพร่ข้อมูล
publisher = context.socket(zmq.PUB)

# bind socket เข้ากับพอร์ต 5555 ทุก IP (0.0.0.0) บนเครื่อง
# ทำให้ subscriber สามารถเชื่อมต่อเข้ามาฟังได้
publisher.bind("tcp://*:5555")

# ให้เวลาสำหรับ subscriber ที่กำลังเชื่อมต่ออยู่
time.sleep(1)

while True:
    topic = "msg1"  # Topic ของข้อความ (subscriber ต้อง subscribe ตามหัวข้อนี้)
    message = "Hello from original publisher"  # เนื้อหาข้อความ
    full_message = f"{topic} {message}"  # ต้องรวม topic และ message เข้าด้วยกัน เพราะ ZMQ แยกไม่ให้โดยอัตโนมัติ

    print("📤 กำลังส่ง:", full_message)
    publisher.send_string(full_message)  # ส่งข้อความเป็น string (ZMQ รองรับ binary ด้วย)
    time.sleep(1)  # ส่งทุก 1 วินาที
