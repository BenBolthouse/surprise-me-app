/** @module services/socket */

/* eslint-disable no-undef */

import { io } from "socket.io-client";
import { store } from "../index";
import { composingMessage } from "../store/reducers/connections";
import { receiveMessage, amendMessage, discardMessage } from "../store/reducers/messages";

const DEBUG = process.env.NODE_ENV === "development";

let created = false;

/**
 * @class
 * @classdesc Service class provides connection to the socketio host.
 */
class Socket {
  /** @returns {this} */
  constructor() {
    if (created) throw new Error("Cannot create instance of singleton class");

    this.connected = false;

    this.client = null;

    created = true;

    return this;
  }

  /**
   * Connects the client to a socket for sending/receiving messages.
   */
  connect() {
    this.connected = true;

    this.client = _init();
  }

  /**
   * Disconnects the client from the socket.
   */
  disconnect() {
    if (DEBUG) console.log("SocketIO client: Client has disconnected");

    this.connected = false;

    this.client = this.client.disconnect();
  }

  /**
   * Joins the user to a room.
   */
  joinRoom(roomName) {
    if (!this.client) {
      throw Error("Client not initialized");
    }

    this.client.emit("join", { room_id: roomName });
  }

  /**
   * Determines if a socket connection is established, and if not then connects the client.
   */
  require() {
    if (!this.connected) this.connect();
  }
}

/**
 * Private function configures the socket client and adds event listeners.
 *
 * @returns {object} client
 */
function _init() {
  const client = io("");

  const userId = store.getState().session.id;

  // Following section handles configuring this service for use in a
  // debugging environment.
  if (DEBUG) {
    window.socketioClient = client;

    client.on("message", (message) => console.log("SocketIO host: " + message));
  }

  // User's default rooms on joining a session.
  client.emit("join", { room_id: `message_room_${userId}` });
  client.emit("join", { room_id: `notifications_room_${userId}` });

  // Listeners for events trigger Redux reducer actions, and are all listed here.
  client.on("deliver_message", (payload) => store.dispatch(receiveMessage(payload)));
  client.on("amend_message", (payload) => store.dispatch(amendMessage(payload)));
  client.on("discard_message", (payload) => store.dispatch(discardMessage(payload)));
  client.on("composing_message", (payload) => store.dispatch(composingMessage(payload)));

  // Event emitters are also loaded onto the Socketio client object and are
  // callable by importing the client into app components.
  client.composeMessage = function (connectionId, composing) {
    client.emit("composing_message", { connection_id: connectionId, composing })
  }

  return client;
}

export default Socket;
