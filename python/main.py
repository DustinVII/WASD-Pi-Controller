import socketio
import gpiozero


node_server = "http://dustinpizero:3000"

led_w = gpiozero.LED(4)
led_s = gpiozero.LED(17)
led_d = gpiozero.LED(27)
led_a = gpiozero.LED(22)




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
    action = data.get("action")

    if key == "w":
        if action == "down":
            print(f"Move forward")
            led_w.on()
        else:
            led_w.off()
    elif key == "a":
        if action == "down":
            print(f"Move left")
            led_a.on()
        else:
            led_a.off()
    elif key == "s":
        if action == "down":
            print(f"Move backward")
            led_s.on()
        else:
            led_s.off()
    elif key == "d":
        if action == "down":
            print(f"Move right")
            led_d.on()
        else:
            led_d.off()


if sio.connected:
    sio.wait()