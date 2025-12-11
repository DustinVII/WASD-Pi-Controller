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
pip install -r requirements.txt
python main.py
```
7. Open `index.php` in your browser and start controlling with the keys.

## Setup for online web servers over HTTPS:
Below is the correct Apache setup for HTTPS → HTTP upgrade support, which Socket.IO requires.

### 1. In Node.js server `server.js` change:

**Before**
```js
httpServer.listen(3000);
```
**Changes made**

Added `0.0.0.0` to bind all interfaces:

```js
httpServer.listen(3000, "0.0.0.0", () => {
    console.log("Socket.io server running on port 3000!");
});
```
This keeps the server HTTP only, no SSL inside Node.js. **Reason**: SSL will be terminated by Apache → simpler, easier to manage. Result: Node.js server still listens on HTTP 3000 internally, accessible by Apache.

### 2. Frontend JavaScript `script.js` changes
**Before**:
```js
const socket = io("https://dustinpi:3000");
```

**Changes made**:
```js
const socket = io(); // Automatically uses current domain + protocol
```
**Result**: Browser connects via HTTPS to Apache, which proxies to Node.js.

### 3. Apache configuration changes

If using Apache, a reverse proxy with WebSocket support is required.

#### 3.1 Enable required Apache modules
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_wstunnel
sudo a2enmod rewrite
sudo systemctl restart apache2
```
These modules allow Apache to forward WebSockets correctly.
Node.js server needs to be running on HTTP (behind Apache SSL proxy).

#### 3.2 Port 80 VirtualHost `/etc/apache2/sites-available/yoursubd.yoursite.com.conf`

```apache
<VirtualHost *:80>
    ServerName yoursubd.yoursite.com
    ServerAlias www.yoursubd.yoursite.com

    RewriteEngine On
    RewriteRule ^ https://yoursubd.yoursite.com%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```

This only redirects HTTP → HTTPS. No DocumentRoot needed. Prevents redirect loops

#### 3.3 Port 443 SSL VirtualHost `/etc/apache2/sites-available/yoursubd.yoursite.com.conf`
Enable WebSocket upgrade headers. ProxyPassMatch handle `/socket.io` with or without trailing slash. SSL certificates correctly referenced.

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName yoursubd.yoursite.com
    ServerAlias www.yoursubd.yoursite.com

    DocumentRoot /var/www/html

    <Directory /var/www/html>
        AllowOverride All
        Require all granted
    </Directory>

    # ------------------------------
    # Socket.IO + WebSocket Reverse Proxy
    # ------------------------------
    ProxyPreserveHost On

    RewriteEngine On

    # WebSocket Upgrade
    RewriteCond %{HTTP:Upgrade} =websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/socket.io/(.*) ws://localhost:3000/socket.io/$1 [P,L]

    # Proxy normal Socket.IO requests (with or without trailing slash)
    ProxyPassMatch "^/socket.io(.*)$" "http://localhost:3000/socket.io$1"

    # ------------------------------
    # SSL Certificates
    # ------------------------------
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yoursubd.yoursite.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yoursubd.yoursite.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```

### 4. Python client `main.py` changes
**Before**:
```python
node_server = "http://dustinpizero:3000"
sio.connect(node_server)
```

Problems with this is:

- Node server only accessible via Apache HTTPS proxy
- Python client default transport (polling) sometimes fails over HTTPS proxy
- Path /socket.io not specified → Apache will give 503

**After**:
```python
node_server = "https://yoursubd.yoursite.com"

sio.connect(
    node_server,
    transports=["websocket"],
    socketio_path="/socket.io/"
)
```

**Why this works**: `transports=["websocket"]` → forces WebSocket transport through Apache. `socketio_path="/socket.io/"` → ensures correct path for reverse proxy. Works with Apache SSL proxy.

### 5. Final architecture:
```css
[Browser HTTPS] ---> [Apache SSL Proxy /socket.io] ---> [Node.js HTTP 3000]
[Python HTTPS] ---> [Apache SSL Proxy /socket.io] ---> [Node.js HTTP 3000]
```
- Node.js never needs SSL
- Frontend + Python client can both connect securely
- WebSocket upgrades work correctly
- Mixed content errors are eliminated



## Requirements

- [Node.js](https://nodejs.org/) with NPM
- Node server running on a Raspberry Pi or any network-accessible machine
- [Python](https://www.python.org/downloads/)
- Optional: RPi.GPIO or gpiozero (if you want to control LEDs, motors, etc.)
- Raspberry Pi (any model with Python 3)