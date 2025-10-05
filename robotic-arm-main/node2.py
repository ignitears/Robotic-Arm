import zmq
import json
import time
from pyfirmata2 import Arduino

COM_PORT = "COM5"
SERVO_PINZ = 'd:9:s'
SERVO_PINGrab = 'd:8:s'
SERVO_PINA1 = 'd:10:s'
SERVO_PINA2 = 'd:11:s'

INPUT_WIDTH = 640

print(f"🔌 กำลังเชื่อมต่อ Arduino ที่ {COM_PORT} ...")
board = Arduino(COM_PORT)
servoZ = board.get_pin(SERVO_PINZ)
servoZ.write(90)
servoA1 = board.get_pin(SERVO_PINA1)
servoA1.write(45)
servoA2 = board.get_pin(SERVO_PINA2)
servoA2.write(110)


servoGrab = board.get_pin(SERVO_PINGrab)

servoGrab.write(130)
time.sleep(1)
servoGrab.write(40)
print("✅ เชื่อมต่อสำเร็จ, พร้อมควบคุม Servo")

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5555")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "board_shield")
print("📡 Subscriber เชื่อมต่อ tcp://127.0.0.1:5555 topic 'board_shield'")

poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)

try:
    while True:
        socks = dict(poller.poll(200))  # timeout 200 ms
        if subscriber in socks:
            message = subscriber.recv_string(zmq.NOBLOCK)
            topic, json_payload = message.split(' ', 1)

            try:
                data = json.loads(json_payload)
                x = int(data.get("x", -1))
                if x >= 0:
                    angle = max(0, min(180, int((x / INPUT_WIDTH) * 180)))  
                    servoZ.write(angle)
                    print(f"📥 ได้ค่า x={x} → หมุน Servo ไปที่ {angle}°")
            except json.JSONDecodeError:
                print("❌ JSON ไม่ถูกต้อง:", json_payload)
        # loop continues even if no message arrives
except KeyboardInterrupt:
    print("\n🛑 หยุดการทำงานตามคำสั่งผู้ใช้")
finally:
    servoZ.write(90)
    board.exit()
    subscriber.close()
    context.term()
    print("✅ ปิดการเชื่อมต่อและทำความสะอาดเรียบร้อย")
