import { store } from "../../index";
import { fetch } from "../../services/fetch";

import * as connectionsActions from "./connections";
import * as securityActions from "./security";

// State template
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
};

// Return a pointer to current state
const getState = () => store.getState();

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const POST_SESSION = "session/postSession";
/**
 * Establish a session for a user and get the user's data to
 * the Redux store.
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
 * the session data and add to Redux state.
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

const POST_USER = "session/postSessionUser";
/**
 * Create a new user and establish a session.
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
      type: POST_USER,
      payload,
    }))(data)
  );
  return res;
};

const POST_SESSION_GEOLOCATION = "session/postSessionGeolocation";
/**
 * Retrieve the client location from the browser and update
 * Redux and backend state.
 */
export const postSessionGeolocation = () => async (dispatch) => {
  navigator.geolocation.getCurrentPosition(
    async ({ coords }) => {
      await fetch("/api/users", {
        method: "PATCH",
        body: JSON.stringify({
          coordLat: coords.latitude,
          coordLong: coords.longitude,
        }),
      });
      dispatch(
        ((payload) => ({
          type: POST_SESSION_GEOLOCATION,
          payload,
        }))({
          coordLat: coords.latitude,
          coordLong: coords.longitude,
        })
      );
      return true;
    }
  );
};

const CONNECT_SOCKET_CLIENT = "session/connectSocketClient";
/**
 * Connect a websocket connection with the server with a
 * specific room name.
 * 
 * @param {*} clientRoomId Required; usually
 * `session.user.id` for room name. 
 */
export const connectSocketClient = (client) => ({
  type: CONNECT_SOCKET_CLIENT,
  payload: client,
});

const DISCONNECT_SOCKET_CLIENT = "session/disconnectSocketClient";
/**
 * Disconnect the client from the Redux state.
 */
export const disconnectSocketClient = () => ({
  type: DISCONNECT_SOCKET_CLIENT,
});

const JOIN_SOCKET_CLIENT_ROOM = "session/joinSocketClientRoom";

export const joinSocketClientRoom = (roomId) => async (dispatch) => {
  const storeState = getState();
  const client = storeState.session.socketClient;
  client.emit("join", { roomId });
  dispatch(
    ((payload) => ({
      type: JOIN_SOCKET_CLIENT_ROOM,
      payload,
    }))(roomId)
  );
}

const LEAVE_SOCKET_CLIENT_ROOM = "session/leaveSocketClientRoom";

export const leaveSocketClientRoom = (roomId) => async (dispatch) => {
  const storeState = getState();
  const client = storeState.session.socketClient;
  client.emit("leave", { roomId });
  dispatch(
    ((payload) => ({
      type: LEAVE_SOCKET_CLIENT_ROOM,
      payload,
    }))(roomId)
  );
}

const POST_CHAT_MESSAGE = "session/postChatMessage";

export const postChatMessage = (chatObject) => async (dispatch) => {
  const storeState = getState();
  const client = storeState.session.socketClient;
  client.emit("post_chat_message", chatObject);
  dispatch(
    ((payload) => ({
      type: POST_CHAT_MESSAGE,
      payload,
    }))(chatObject)
  );
}

// Reducer
const reducer = (state = sessionTemplate, { type, payload }) => {
  switch (type) {
    case POST_SESSION:
      return { ...state, user: { ...state.user, ...payload } };

    case DELETE_SESSION:
      return { ...state, user: {} };

    case POST_USER:
      return { ...state, user: { ...state.user, ...payload } };

    case GET_SESSION:
      return { ...state, user: { ...state.user, ...payload } };

    case POST_SESSION_GEOLOCATION:
      return { ...state, user: { ...state.user, ...payload } };

    case CONNECT_SOCKET_CLIENT:
      return { ...state, socketClient: payload };

    case DISCONNECT_SOCKET_CLIENT:
      if(state.socketClient) {
        state.socketClient.disconnect();
      }
      return { ...state, socketClient: null };
    
    case JOIN_SOCKET_CLIENT_ROOM:
      return state;
    
    case LEAVE_SOCKET_CLIENT_ROOM:
      return state;
    
    case POST_CHAT_MESSAGE:
      return state;

    default:
      return state;
  }
};

export default reducer;
