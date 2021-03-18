import { fetch } from "../../services/fetch";

import * as securityActions from './security'

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

const LOGIN_SESSION_USER = "session/loginSessionUser";
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
      type: LOGIN_SESSION_USER,
      payload,
    }))(data)
  );
  return data;
};

const LOGOUT_SESSION_USER = "session/logoutSessionUser";
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
      type: LOGOUT_SESSION_USER,
      payload,
    }))(data)
  );
  dispatch(securityActions.getXCsrfToken())
  return res;
};

const POST_SESSION_USER = "session/postSessionUser";
/**
 * Create a new user and establish a session.
 *
 * @param {*} userObject Contains all of the parameters for
 * a new user.
 */
export const postSessionUser = (userObject) => async (dispatch) => {
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

const GET_SESSION_USER = "session/getSessionUser";
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
      type: GET_SESSION_USER,
      payload,
    }))(data)
  );
  return res;
};

// Reducer
const reducer = (state = { user: userTemplate }, { type, payload }) => {
  switch (type) {
    case LOGIN_SESSION_USER:
      return { user: { ...state.user, ...payload } };

    case LOGOUT_SESSION_USER:
      return { user: {} };

    case POST_SESSION_USER:
      return { user: { ...state.user, ...payload } };

    case GET_SESSION_USER:
      return { user: { ...state.user, ...payload } };

    default:
      return state;
  }
};

export default reducer;
