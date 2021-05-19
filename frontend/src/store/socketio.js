/* eslint-disable no-undef */

import { io } from "socket.io-client";

const production = process.env.NODE_ENV === "production";

const socketClient = io({ autoConnect: false });

if (!production) {
  socketClient.on("message", (msg) => console.log("Socketio Host:", msg));
}

export default socketClient;
