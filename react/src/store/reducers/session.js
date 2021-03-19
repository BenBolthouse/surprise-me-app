import { fetch } from "../../services/fetch";

import * as securityActions from "./security";

// State template
const userTemplate = {
  id: null,
  firstName: null,
  lastName: null,
  email: null,
  shareLocation: null,
  coordLat: null,
  coordLong: null,
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

export const postSessionGeolocation = () => async (dispatch) => {
  let geolocation;
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
          type: POST_USER,
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

// Reducer
const reducer = (state = { user: userTemplate }, { type, payload }) => {
  switch (type) {
    case POST_SESSION:
      return { user: { ...state.user, ...payload } };

    case DELETE_SESSION:
      return { user: {} };

    case POST_USER:
      return { user: { ...state.user, ...payload } };

    case GET_SESSION:
      return { user: { ...state.user, ...payload } };

    case POST_SESSION_GEOLOCATION:
      return { user: { ...state.user, ...payload } };

    default:
      return state;
  }
};

export default reducer;
