import zmq, json, time
ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)
pub.bind("tcp://*:5555")
time.sleep(1)  # wait for subscriber to connect

while True:
    msg = json.dumps({"x": 320})
    pub.send_string(f"board_shield {msg}")
    print("Sent test data:", msg)
    time.sleep(1)
