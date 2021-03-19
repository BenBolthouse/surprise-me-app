import { io } from "socket.io-client";

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
  dispatch(postSessionGeolocation());
  dispatch(connectionsActions.getConnections());
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
export const connectSocketClient = (clientRoomId) => ({
  type: CONNECT_SOCKET_CLIENT,
  payload: clientRoomId,
});

// Reducer
const reducer = (state = sessionTemplate, { type, payload }) => {
  switch (type) {
    case POST_SESSION:
      return { ...state, user: { ...state.user, ...payload } };

    case DELETE_SESSION:
      return { user: {} };

    case POST_USER:
      return { ...state, user: { ...state.user, ...payload } };

    case GET_SESSION:
      return { ...state, user: { ...state.user, ...payload } };

    case POST_SESSION_GEOLOCATION:
      return { ...state, user: { ...state.user, ...payload } };

    case CONNECT_SOCKET_CLIENT:
      const transports = process.env.NODE_ENV === "development"
          ? ["polling"]
          : ["polling", "websockets"];
      const client = io(process.env.REACT_APP_HOST_NAME, {
        transports: transports,
      });
      return { ...state, socketClient: client };

    default:
      return state;
  }
};

export default reducer;
