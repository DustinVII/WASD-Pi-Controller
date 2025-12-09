import { Server } from "socket.io";
import http from "http";

// Create a plain HTTP server
const httpServer = http.createServer();
const io = new Server(httpServer, { cors: { origin: "*" } });


io.on("connection", (socket) => {

    socket.on("move", (data) => {
        console.log("Movement key:", data.key);
        io.emit("movement-command", data); // Send to Python
    });

});

httpServer.listen(3000, () => {
    console.log("Socket.io server running on port 3000, listening on all interfaces!");
  });