import { io } from "socket.io-client";

const socket = io();

socket.on("connect", () => {
    console.log("🔥 CONNECTED:", socket.id);
});

socket.on("disconnect", (reason) => {
    console.log("🔥 DISCONNECTED:", socket.id, reason);
});

socket.on("connect_error", (error) => {
    console.log("🔥 SOCKET ERROR:", error.message);
});

socket.onAny((event, ...args) => {
    console.log("🔥 EVENT:", event, args);
});

export default socket;