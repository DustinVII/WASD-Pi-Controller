import socketio
import gpiozero
from time import sleep
import atexit

# --- Notes ---
# Force global socketio install with the following command (not recommended for beginners)
# sudo pip3 install "python-socketio[client]" --break-system-packages

# --- Node server configuration ---
# node_server = "http://dustinpizero:3000"
node_server = "https://aws.dulamari.com" # Example for online server


# === LEDs and sensor ===
led_w = gpiozero.LED(4)
led_s = gpiozero.LED(17)
led_d = gpiozero.LED(27)
led_a = gpiozero.LED(22)

# === Cleanup function ===
def cleanup():
    led_w.off()
    led_s.off()
    led_d.off()
    led_a.off()
    print("Cleaned up GPIO.")

atexit.register(cleanup)

# --- Socket.IO client setup ---
sio = socketio.Client()

@sio.event
def connect():
    print(f"Connected to Node server: {node_server}")

@sio.event
def disconnect():
    print(f"Disconnected from Node server: {node_server}")

@sio.on("movement-command")
def movement(data):
    key = data.get("key")
    action = data.get("action")

    if key == "w":
        led_w.on() if action == "down" else led_w.off()
        print("Move forward" if action == "down" else "")
    elif key == "a":
        led_a.on() if action == "down" else led_a.off()
        print("Move left" if action == "down" else "")
    elif key == "s":
        led_s.on() if action == "down" else led_s.off()
        print("Move backward" if action == "down" else "")
    elif key == "d":
        led_d.on() if action == "down" else led_d.off()
        print("Move right" if action == "down" else "")

# --- Connect to server ---
try:
    sio.connect(
        node_server,
        transports=["websocket"],
        socketio_path="/socket.io/"
    )
except Exception as e:
    print(f"Failed to connect to Node server {node_server}:", e)
    exit(1)


# --- Keep Socket.IO client running ---
try:
    sio.wait()
except KeyboardInterrupt:
    print("Exiting Socket.IO client...")