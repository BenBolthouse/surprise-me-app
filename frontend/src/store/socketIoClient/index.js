/* eslint-disable no-undef */

import { io } from "socket.io-client";

const production = process.env.NODE_ENV === "production";

export const socketIoClient = io({ autoConnect: false });

if (!production) {
  socketIoClient.on("message", (msg) => console.log("Socketio Host:", msg));
}
