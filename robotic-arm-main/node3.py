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
Direction = 90
magic_plusNumber = 10
LeftOrRight = 0 #0 = left

print(f"🔌 กำลังเชื่อมต่อ Arduino ที่ {COM_PORT} ...")
board = Arduino(COM_PORT)
time.sleep(1)
servoZ = board.get_pin(SERVO_PINZ)
#servoZ.write(90)
servoA1 = board.get_pin(SERVO_PINA1)

servoA2 = board.get_pin(SERVO_PINA2)
servoGrab = board.get_pin(SERVO_PINGrab)
servoA2.write(45)

servoGrab.write(180)
time.sleep(1)
servoGrab.write(90)
time.sleep(1)
servoA2.write(45)
time.sleep(1)
servoGrab.write(180)

print("✅ เชื่อมต่อสำเร็จ, พร้อมควบคุม Servo")

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5555")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "board_shield")
print("📡 Subscriber เชื่อมต่อ tcp://127.0.0.1:5555 topic 'board_shield'")

poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)

def yolo_find(target_name: str):

    socks = dict(poller.poll(200))  # wait up to 200 ms for a message
    if subscriber in socks:
        message = subscriber.recv_string(zmq.NOBLOCK)
        topic, json_payload = message.split(' ', 1)

        try:
            data = json.loads(json_payload)
            obj_name = data.get("name")  # <-- assumes publisher sends name in JSON
            if obj_name == target_name:
                return True
        except json.JSONDecodeError:
            print("❌ JSON ไม่ถูกต้อง:", json_payload)
    return False

def yolo_find_until_left(threshold_px=10):
    
    while True:
        socks = dict(poller.poll(200))  # wait up to 200 ms
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
                    global Direction
                    Direction = angle
                    if x <= threshold_px:
                        print(f"✅ x={x} is very close to 0, stopping.")
                        return x
            except json.JSONDecodeError:
                print("❌ JSON ไม่ถูกต้อง:", json_payload)

def scan_what_to_stored(What):
    for i in range(180):
        servoZ.write(i)
        Validation = yolo_find(What)
        if Validation == True:
            yolo_find_until_left()
        i += 1
        time.sleep(0.02)

def turn(value):
    pass
    global Direction
    if value >=0:
        for i in range(value):
            Direction += i
            servoZ.write(Direction)
            time.sleep(0.2)
    else:
        value *= -1
        for i in range(value):
            Direction -= i
            servoZ.write(Direction)
            time.sleep(0.2)
def keep():
    A2 = 60
    #A2 = 30
    A2a = 90 - A2
    """
    A2a = 90 - A2
    for i in range(A2a):
        j = 90-i
        servoA2.write(j)
    """
    for i in range(45):
        j = 45 + i
        servoA2.write(j)
        time.sleep(0.02)

    servoGrab.write(40)
    time.sleep(1)
    for i in range(45):
        j = 90-i
        servoA2.write(j)
        time.sleep(0.02)
    





# time.sleep(1)
# servoZ.write()
time.sleep(1)
servoZ.write(0)
time.sleep(1)
servoA2.write(85)
time.sleep(1)
servoZ.write(135)




for i in range(90):
    pass


def reverse_keep():
    A1 = 60
    A1a = 90 - A1
    for i in range(45):
        j = 90 - i
        servoA2.write(j)
        time.sleep(0.02)

    servoGrab.write(130)
    for i in range(45):
        j = i + 45
        servoA2.write(j)
        time.sleep(0.02)

servoA2.write(45)
for i in range(90):
    j = 90-i
    servoZ.write(j)
    time.sleep(0.02)
servoZ.write(0)
servoA2.write(90)

servoGrab.write(180)
time.sleep(1)
servoA2.write(90)
servoGrab.write(90)
time.sleep(1)
for i in range(90):
    j = i
    servoZ.write(0)
    time.sleep(0.02)
time.sleep(2)
servoA2.write(45)
time.sleep(1)
servoGrab.write(180)

"""
scan_what_to_stored("donut_red")

if Direction <= 140:
    turn(Direction-magic_plusNumber)
    LeftOrRight = 1
else:
    turn(Direction+magic_plusNumber)
    LeftOrRight = 0
keep()

scan_what_to_stored("base")
if LeftOrRight == 0:
    turn(Direction-magic_plusNumber)
else:
    turn(Direction+magic_plusNumber)
reverse_keep()
scan_what_to_stored("donut_green")
if Direction <= 140:
    turn(Direction-magic_plusNumber)
    LeftOrRight = 1
else:
    turn(Direction+magic_plusNumber)
    LeftOrRight = 0
keep()
scan_what_to_stored("base")
if LeftOrRight == 0:
    turn(Direction-magic_plusNumber)
else:
    turn(Direction+magic_plusNumber)
reverse_keep()
scan_what_to_stored("donut_blue")
if Direction <= 140:
    turn(Direction-magic_plusNumber)
    LeftOrRight = 1
else:
    turn(Direction+magic_plusNumber)
    LeftOrRight = 0
keep()

scan_what_to_stored("base")
if LeftOrRight == 0:
    turn(Direction-magic_plusNumber)
else:
    turn(Direction+magic_plusNumber)
reverse_keep()
"""
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
