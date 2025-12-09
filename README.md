# WASD Pi Controller

WASD Pi Controller is a lightweight browser-based control system for the Raspberry Pi. It captures WASD keyboard input from any device on your network and sends the commands in real time to a Node.js Socket.io server, which relays them to a Python client running on the Raspberry Pi.

This makes it perfect for robotics, LED control, small vehicles or any project where you want fast, low-latency directional input—just like in a game.

## Features

- Real-time keyboard input (W, A, S, D)
- Minimalistic front-end UI with key highlight animations
- Socket.io communication between browser → Node.js → Raspberry Pi
- Python client receives movement commands instantly
- Easy to expand for GPIO/LED/motor control

## Installation
1. Clone project to your Raspberry Pi
```bash
git clone https://github.com/DustinVII/WASD-Pi-Controller.git
```
2. Set the correct host and port number in `/js/script.js`.
3. Set the correct port in `node/server.js`.
4. Install Node dependencies and start Node server in a new terminal
```bash
cd node
npm install
node server.js
```
5. Create new Python virtual environment and activate it
```bash
cd python
python -m venv myvenv
source myvenv/bin/activate
```
6. Install Python dependencies and start Python `main.py` script
```bash
pip install -r package.txt
python main.py
```
7. Open `index.php` in your browser and start controlling with the keys.

## Requirements

- [Node.js](https://nodejs.org/) with NPM
- Node server running on a Raspberry Pi or any network-accessible machine
- [Python](https://www.python.org/downloads/)
- Optional: RPi.GPIO or gpiozero (if you want to control LEDs, motors, etc.)
- Raspberry Pi (any model with Python 3)