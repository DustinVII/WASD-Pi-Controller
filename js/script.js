 // Connect to your Socket.io server
 const socket = io("http://dustinpizero:3000");

 // Map keys to HTML elements
 const keyMap = {
     "w": $("#key-w"),
     "a": $("#key-a"),
     "s": $("#key-s"),
     "d": $("#key-d")
 };

 // KeyDown event
 $(document).on("keydown", function (e) {
     const key = e.key.toLowerCase();
     if (!keyMap[key]) return;

     keyMap[key].addClass("active");
     socket.emit("move", { key: key, action: "down" });
     console.log("Pressed:", key);
 });

 // KeyUp event
 $(document).on("keyup", function (e) {
     const key = e.key.toLowerCase();
     if (!keyMap[key]) return;

     keyMap[key].removeClass("active");
     socket.emit("move", { key: key, action: "up" });
     console.log("Released:", key);
 });