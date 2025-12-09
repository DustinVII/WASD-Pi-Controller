 // Connect to your Socket.io server
 const socket = io("http://dustinpi:3000");

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
     socket.emit("move", { key: key });
     console.log("Pressed:", key);
 });

 // KeyUp event
 $(document).on("keyup", function (e) {
     const key = e.key.toLowerCase();
     if (!keyMap[key]) return;

     keyMap[key].removeClass("active");
 });