import { store } from "../../index";
import { fetch } from "../../services/fetch";

import * as securityActions from "./security";

// Reducer template
const sessionTemplate = {
  user: {
    id: null,
    firstName: null,
    lastName: null,
    email: null,
    shareLocation: null,
    coordLat: null,
    coordLong: null,
  },
  socketClient: null,
  socketConnectedRoomId: null,
};

/**
 * Get the current state.
 */
const getState = () => store.getState();

// ** «««««««««««««««««««««««« Session User Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const POST_SESSION_USER = "session/postSessionUser";
/**
 * Create a new user; establish a session and persist user
 * data to the Redux store.
 *
 * @param {*} userObject Contains all of the parameters for
 * a new user.
 */
export const createNewUser = (userObject) => async (dispatch) => {
  const res = await fetch("/api/users", {
    method: "POST",
    body: JSON.stringify(userObject),
  });
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: POST_SESSION_USER,
      payload,
    }))(data)
  );
  return res;
};

const POST_SESSION = "session/postSession";
/**
 * Establish a session for a user and persist the user's
 * data to the Redux store.
 *
 * @param {*} object Contains required arguments string
 * **email** and string **password**.
 */
export const loginSessionUser = ({ email, password }) => async (dispatch) => {
  const res = await fetch("/api/sessions", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: POST_SESSION,
      payload,
    }))(data)
  );
  return data;
};

const GET_SESSION = "session/getSession";
/**
 * Assuming that the client holds a session token, retrieve
 * the session data and persist to the Redux store.
 */
export const getSessionUser = () => async (dispatch) => {
  const res = await fetch("/api/sessions", {
    method: "GET",
  });
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: GET_SESSION,
      payload,
    }))(data)
  );
  return res;
};

const DELETE_SESSION = "session/deleteSession";
/**
 * Remove the session for the user and clear Redux state.
 */
export const logoutSessionUser = () => async (dispatch) => {
  const res = await fetch("/api/sessions", {
    method: "DELETE",
  });
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: DELETE_SESSION,
      payload,
    }))(data)
  );
  dispatch(disconnectSocketClient());
  dispatch(securityActions.getXCsrfToken());
  return res;
};

// ** ««««««««««««««««««««« Client Geolocation Actions »»»»»»»»»»»»»»»»»»»»» **

const PATCH_SESSION_GEOLOCATION = "session/patchSessionGeolocation";
/**
 * Retrieve the client location from the browser and update
 * the Redux store and host database.
 */
export const patchSessionGeolocation = () => async (dispatch) => {
  navigator.geolocation.getCurrentPosition(async ({ coords }) => {
    await fetch("/api/users", {
      method: "PATCH",
      body: JSON.stringify({
        coordLat: coords.latitude,
        coordLong: coords.longitude,
      }),
    });
    dispatch(
      ((payload) => ({
        type: PATCH_SESSION_GEOLOCATION,
        payload,
      }))({
        coordLat: coords.latitude,
        coordLong: coords.longitude,
      })
    );
    return true;
  });
};

// ** ««««««««««««««««««««« Client Websockets Actions »»»»»»»»»»»»»»»»»»»»» **

const CONNECT_SOCKET_CLIENT = "session/connectSocketClient";
/**
 * Establish a Socketio connection.
 *
 * @param {*} client Socketio client using `io.connect(...)`.
 */
export const connectSocketClient = (client) => ({
  type: CONNECT_SOCKET_CLIENT,
  payload: client,
});

const DISCONNECT_SOCKET_CLIENT = "session/disconnectSocketClient";
/**
 * Disconnect the Socketio client.
 */
export const disconnectSocketClient = () => ({
  type: DISCONNECT_SOCKET_CLIENT,
});

const JOIN_SOCKET_CLIENT_ROOM = "session/joinSocketClientRoom";
/**
 * Connect to a Socketio room on the host.
 *
 * @param {*} roomId Integer room ID.
 */
export const joinSocketClientRoom = (roomId) => async (dispatch) => {
  const storeState = getState();
  const client = storeState.session.socketClient;
  dispatch(
    ((payload) => ({
      type: JOIN_SOCKET_CLIENT_ROOM,
      payload,
    }))(roomId)
  );
};

const LEAVE_SOCKET_CLIENT_ROOM = "session/leaveSocketClientRoom";
/**
 * Leave a Socketio room on the host.
 *
 * @param {*} roomId Integer room ID.
 */
export const leaveSocketClientRoom = (roomId) => async (dispatch) => {
  const storeState = getState();
  const client = storeState.session.socketClient;
  client.emit("leave", { roomId });
  dispatch(
    ((payload) => ({
      type: LEAVE_SOCKET_CLIENT_ROOM,
      payload,
    }))()
  );
};

// ** «««««««««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = sessionTemplate, { type, payload }) => {
  switch (type) {
    case POST_SESSION:
      return { ...state, user: { ...state.user, ...payload } };

    case DELETE_SESSION:
      return { ...state, user: {} };

    case POST_SESSION_USER:
      return { ...state, user: { ...state.user, ...payload } };

    case GET_SESSION:
      return { ...state, user: { ...state.user, ...payload } };

    case PATCH_SESSION_GEOLOCATION:
      return { ...state, user: { ...state.user, ...payload } };

    case CONNECT_SOCKET_CLIENT:
      return { ...state, socketClient: payload };

    case DISCONNECT_SOCKET_CLIENT:
      if (state.socketClient) {
        state.socketClient.disconnect();
      }
      return { ...state, socketClient: null };

    case JOIN_SOCKET_CLIENT_ROOM:
      return {...state, socketConnectedRoomId: payload};

    case LEAVE_SOCKET_CLIENT_ROOM:
      return {...state, socketConnectedRoomId: null};

    default:
      return state;
  }
};

export default reducer;
