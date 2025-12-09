import socketio

node_server = "http://dustinpi:3000"

sio = socketio.Client()

try:
    sio.connect(node_server)
    if sio.connected:
        print(f"Successfully connected to Node server: {node_server}")
    else:
        print(f"Failed to connect to Node server: {node_server}")
except Exception as e:
    print(f"Connection to Node server {node_server} failed:", e)

@sio.on("movement-command")
def movement(data):
    key = data.get("key")
    print("Received movement:", key)

    if key == "w":
        print("Move forward")
    elif key == "a":
        print("Move left")
    elif key == "s":
        print("Move backward")
    elif key == "d":
        print("Move right")

if sio.connected:
    sio.wait()